from operator import itemgetter
from typing import Any, Dict, Literal, Tuple, Union

import torch
from detectools import Task
from detectools.formats import BatchedFormats, SegmentationFormat
from detectools.models import BaseModel
from torch import Tensor
from torchvision.ops import masks_to_boxes
from detectools.formats.detect_mask import DetectMask
from transformers import (
    Mask2FormerConfig,
    Mask2FormerForUniversalSegmentation,
    Mask2FormerImageProcessor,
)
from transformers.models.mask2former.modeling_mask2former import (
    Mask2FormerForUniversalSegmentationOutput,
)


class Mask2Former(Mask2FormerForUniversalSegmentation, BaseModel):
    """Mask2Former model class in detectools. This class inheriths from Mask2FormerForUniversalSegmentation_ (HuggingFace, transformers) and BaseModel (detectools).
    Construct Mask2Former model from huggingface/transformer model architectures.
        
    .. _Mask2FormerForUniversalSegmentation:
            https://huggingface.co/docs/transformers/model_doc/mask2former

    Args:
        num_classes (``int``, **optional**): Number of classes. Defaults to 1.
        pretrain (``Literal['large', 'medium', 'small', 'tiny']``, **optional**): Size of the pretrained model. Defaults to "tiny".
        overlap_mask_thr (``float``, **optional**):  Mask threshold to merge masks from Mask2FormerOutput. Defaults to 0.8.

    Attributes:
    -----------

    Attributes:
        confidence_thr (``float``): Confidence score threshold to consider object as true prediction.
        max_detection (``int``): Maximum number of object to predict on one image.
        nms_threshold (``float``): IoU threshold to consider 2 boxes as overlapping for Non Max Suppression algorithm.
        num_classes (``int``): Number of classes. 
        size_configs (``Dict[str, str]``): Dict of existing depth configuration for Mask2Former.
    
    Methods:
    -----------
    """

    confidence_thr: float = 0.5
    max_detection: int = 300
    nms_threshold: float = 0.45
    num_classes: int = 1
    overlap_mask_thr: float = 0.8

    # different model size from huggingface
    size_configs = {
        "large": "facebook/mask2former-swin-large-coco-instance",
        "medium": "facebook/mask2former-swin-base-coco-instance",
        "small": "facebook/mask2former-swin-small-coco-instance",
        "tiny": "facebook/mask2former-swin-tiny-coco-instance",
    }

    def __init__(
        self,
        num_classes: int = 1,
        pretrain: Literal["large", "medium", "small", "tiny"] = "tiny",
        overlap_mask_thr: float = 0.8,
    ):
        
        # assert Task mode is "instance_segmentation"
        assert (
            Task.mode == "instance_segmentation"
        ), f"Task mode should be 'instance_segmentation' to construct Mask2Former object, got {Task.mode}"

        if pretrain:
            pretrain_config = Mask2Former.size_configs[pretrain]
            pretrain_model = Mask2FormerForUniversalSegmentation.from_pretrained(
                pretrain_config,
                num_labels=num_classes + 1,
                ignore_mismatched_sizes=True,
            )
            self.__dict__ = pretrain_model.__dict__
        else:
            super().__init__(Mask2FormerConfig(num_classes))

        # define mask2former input processor
        self.processor = Mask2FormerImageProcessor(
            do_resize=False, do_normalize=False, do_rescale=False, ignore_index=255
        )

        self.overlap_mask_thr = overlap_mask_thr
        self.num_classes = num_classes

    def to_device(self, device: Literal["cpu", "cuda"]):
        """Send model to device.

        Args:
            device (``Literal['cpu', 'cuda']``): Device to send model on.
        """
        self.to(device)

    def prepare_target(
        self, target: SegmentationFormat
    ) -> Tuple[Tensor, Dict[int, int]]:
        """Prepare targets for Mask2Former model.

        Args:
            target (``SegmentationFormat``): Target.

        Returns:
            ``Tuple[Tensor, Dict[int, int]]``:
                - Segmentation map.
                - Dict of correspondance {object_id : object_label}.
        """

        labels = target.get("labels").clone()
        labels = torch.cat([torch.tensor([0], device=labels.device), labels + 1])
        instance_labels_dict = dict(zip(range(0, target.size + 1), labels.tolist()))
        masks = target.get("masks")._mask.clone()

        return masks, instance_labels_dict

    def prepare(
        self, images: Tensor, targets: BatchedFormats = None
    ) -> Dict[str, Union[Tensor, Dict[Any, Any]]]:
        """Transform images and targets into Mask2Former specific format for prediction & loss computation.

        Args:
            images (``Tensor``): Batch images.
            targets (``BatchedFormats``, **optional**): Batched targets from DetectionDataset.

        Returns:
            ``Union[Any, Tuple[Any]]``:
                - Images data prepared for Mask2Former.
                - If targets: images + targets prepared for Mask2Former.
        """

        if targets:
            instance_labels = []
            segmentation_maps = []
            for target in targets.formats.values():
                target_masks, target_dict = self.prepare_target(target)
                instance_labels.append(target_dict)
                segmentation_maps.append(target_masks)

            model_input = self.processor(
                images=list(images.unbind()),
                segmentation_maps=segmentation_maps,
                instance_id_to_semantic_id=instance_labels,
                return_tensors="pt",
            )
        else:
            model_input = self.processor(
                images=list(images.unbind()),
                return_tensors="pt",
            )

        return model_input

    def build_boxes(self, masks: Tensor) -> Tensor:
        """Build boxes from segmentation mask.

        Args:
            masks (``Tensor``): Segmentation mask.

        Returns:
            ``Tensor``:
                - Boxes (N, 4).
        """
        # do not infer boxes from background pixels (-1)
        mask_values = torch.unique(masks)
        if -1 in mask_values:
            mask_values = mask_values[1:]

        boxes = []
        for id in mask_values:
            boxes.append(masks_to_boxes((masks == id).unsqueeze(0)))

        return torch.cat(boxes) if len(boxes) else torch.tensor([[]])

    # override
    def build_results(
        self,
        raw_outputs: Mask2FormerForUniversalSegmentationOutput,
        spatial_size: Tuple[int, int],
    ) -> BatchedFormats:
        """Transform model outputs into BatchedFormats for results.

        Args:
            raw_outputs (``Mask2FormerForUniversalSegmentationOutput``): Mask2Former output.
            spatial_size (``Tuple[int, int]``): Size of original image (H, W).

        Returns:
            ``BatchedFormats``:
                - Model output as BatchedFormats.
        """
        # Process raw output wtih Mask2Former processor.
        batch_size = raw_outputs.masks_queries_logits.shape[0]
        predictions = self.processor.post_process_instance_segmentation(
            raw_outputs,
            overlap_mask_area_threshold=self.overlap_mask_thr,
            threshold=self.confidence_thr,
            target_sizes=[spatial_size] * batch_size,
        )
        device = raw_outputs.masks_queries_logits.device
        results = []
        # iter on predictions
        for prediction in predictions:
            spatial_size = prediction["segmentation"].shape[-2:]
            boxes = self.build_boxes(prediction["segmentation"])
            # if no objects return empty Format
            if not boxes.nelement():
                results.append(SegmentationFormat.empty(spatial_size), device=device)
                continue
            # remove empty segmentation objects (objects with no mask pixels)
            non_empty_segmentation = torch.unique(prediction["segmentation"])
            non_empty_segmentation = (
                non_empty_segmentation[non_empty_segmentation != -1].int().tolist()
            )
            segments = prediction["segments_info"]
            if isinstance(segments, dict):
                segments = [segments]
            if len(non_empty_segmentation) > 1:
                getter = itemgetter(*non_empty_segmentation)
                segments = [*getter(segments)]
            else:
                segments = [segments[non_empty_segmentation[0]]]
            # decrease mask values to avoid empty values
            mask = prediction["segmentation"].int()
            mask[mask != -1] += 1
            mask[mask == -1] = 0
            object_id = 1
            for v in torch.unique(mask):
                if v == 0:
                    continue
                mask[mask == v] = object_id
                object_id += 1
                
            labels = torch.tensor([i["label_id"] for i in segments])
            scores = torch.tensor([i["score"] for i in segments])
            

            result = SegmentationFormat(
                spatial_size,
                labels,
                boxes,
                DetectMask(mask),
                scores,
                box_format="XYXY",
            )

            # remove background objects
            result = result[result.get("labels") != 0]
            result.set("labels", result.get("labels") - 1)
            # send boxes to xywh
            result.set_boxes_format("XYWH")
            results.append(result)

        if len(results) == 0:
            results = SegmentationFormat.empty(spatial_size)

        results = BatchedFormats(results)
        return results

    def inputs_to_device(self, input: Any, device: Literal["cpu", "cuda"]):
        """Send Mask2Former inputs to device."""
        for k, v in input.items():
            if isinstance(v, list):
                input[k] = [t.to(device) for t in v]
            elif isinstance(v, Tensor):
                input[k] = v.to(device)

        return input

    def run_forward(
        self, images: Tensor, targets: BatchedFormats, predict: bool = False
    ) -> Union[Dict[str, Tensor], Tuple[Dict[str, Tensor], BatchedFormats]]:
        """Compute loss from images and if target passed, compute loss & return both loss dict
        and results.

        Args:
            images (``Tensor``): Batch RGB images.
            targets (``BatchedFormats``): Batch targets.
            predict (``bool``, **optional**): To return predictions or not. Defaults to False.

        Returns:
            ``Union[Dict[str, Tensor], Tuple[Dict[str, Tensor], BatchedFormats]]``:
                - Loss dict.
                - If predict: Predictions.
        """
        assert predict == (
            not self.training
        ), f"Model mode should be equal to predict boolean, got {self.training} & {predict}"
        # prepare inputs
        spatial_size = images.shape[-2:]
        model_input = self.prepare(images, targets=targets)
        model_input = self.inputs_to_device(model_input, self.device)
        # run forward pass
        output: Mask2FormerForUniversalSegmentationOutput = self(
            pixel_values=model_input["pixel_values"],
            mask_labels=model_input["mask_labels"],
            class_labels=model_input["class_labels"],
        )
        # compute loss
        loss_dict = {"loss": output.loss}
        # return predictions if needed
        if predict:
            predictions = self.build_results(output, spatial_size)
            return loss_dict, predictions
        else:
            return loss_dict

    def get_predictions(self, images: Tensor) -> BatchedFormats:
        """Prepare images, Apply model forward pass and build results.

        Args:
            images (``Tensor``): RGB images Tensor.

        Returns:
            ``BatchedFormats``:
                - Predictions for images as BatchedFormats.
        """
        self.eval()
        spatial_size = images.shape[-2:]
        model_input = self.prepare(images)
        model_input = self.inputs_to_device(model_input, self.device)
        # predict
        output: Mask2FormerForUniversalSegmentationOutput = self(
            pixel_values=model_input["pixel_values"]
        )
        results = self.build_results(output, spatial_size=spatial_size)

        return results
