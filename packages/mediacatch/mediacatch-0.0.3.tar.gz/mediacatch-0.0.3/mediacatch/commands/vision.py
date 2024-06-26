import json
import logging
from argparse import ArgumentParser
from pathlib import Path
from pprint import pprint

from mediacatch.commands import BaseCLICommand
from mediacatch.vision import upload, wait_for_result

logger = logging.getLogger('mediacatch.cli.vision')


def vision_cli_factory(args):
    return VisionCLI(
        file_path=args.file_path,
        type=args.type,
        save_result=args.save_result,
        fps=args.fps,
        tolerance=args.tolerance,
        min_levensthein_ratio=args.min_levensthein_ratio,
        min_bbox_iou=args.min_bbox_iou,
        min_text_confidence=args.min_text_confidence,
        max_text_confidence=args.max_text_confidence,
        max_text_length=args.max_text_length,
        moving_text_threshold=args.moving_text_threshold,
    )


class VisionCLI(BaseCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        vision_parser: ArgumentParser = parser.add_parser(
            'vision', help='CLI tool to run inference with MediaCatch Vision API'
        )
        vision_parser.add_argument(
            'file_path', type=str, help='Path to the file to run inference on'
        )
        vision_parser.add_argument(
            'type',
            type=str,
            choices=['ocr', 'face'],
            help='Type of inference to run on the file',
        )
        vision_parser.add_argument(
            '--save-result',
            type=str,
            default=None,
            help='Save result to a file',
        )
        vision_parser.add_argument(
            '--fps',
            type=int,
            default=None,
            help='FPS for the OCR results',
        )
        vision_parser.add_argument(
            '--tolerance',
            type=int,
            default=None,
            help='Tolerance for the OCR results',
        )
        vision_parser.add_argument(
            '--min-levensthein-ratio',
            type=float,
            default=None,
            help='Minimum Levenshtein ratio for the OCR results',
        )
        vision_parser.add_argument(
            '--min-bbox-iou',
            type=float,
            default=None,
            help='Minimum bounding box IOU for the OCR results',
        )
        vision_parser.add_argument(
            '--min-text-confidence',
            type=float,
            default=None,
            help='Minimum text confidence for the OCR results',
        )
        vision_parser.add_argument(
            '--max-text-confidence',
            type=float,
            default=None,
            help='Maximum text confidence for the OCR results',
        )
        vision_parser.add_argument(
            '--max-text-length',
            type=int,
            default=None,
            help='Maximum text length for the OCR results',
        )
        vision_parser.add_argument(
            '--moving-text-threshold',
            type=int,
            default=None,
            help='Moving text threshold for the OCR results',
        )
        vision_parser.set_defaults(func=vision_cli_factory)

    def __init__(
        self,
        file_path: str,
        type: str,
        save_result: str | None = None,
        fps: int | None = None,
        tolerance: int | None = None,
        min_levensthein_ratio: float | None = None,
        min_bbox_iou: float | None = None,
        min_text_confidence: float | None = None,
        max_text_confidence: float | None = None,
        max_text_length: int | None = None,
        moving_text_threshold: int | None = None,
    ) -> None:
        self.file_path = file_path
        self.type = type
        self.save_result = save_result
        self.fps = fps
        self.tolerance = tolerance
        self.min_levensthein_ratio = min_levensthein_ratio
        self.min_bbox_iou = min_bbox_iou
        self.min_text_confidence = min_text_confidence
        self.max_text_confidence = max_text_confidence
        self.max_text_length = max_text_length
        self.moving_text_threshold = moving_text_threshold

    def run(self) -> None:
        # Create extra parameters
        extra = {}
        for k, val in (
            ('fps', self.fps),
            ('tolerance', self.tolerance),
            ('min_levensthein_ratio', self.min_levensthein_ratio),
            ('min_bbox_iou', self.min_bbox_iou),
            ('min_text_confidence', self.min_text_confidence),
            ('max_text_confidence', self.max_text_confidence),
            ('max_text_length', self.max_text_length),
            ('moving_text_threshold', self.moving_text_threshold),
        ):
            if val is not None:
                extra[k] = val

        # Upload file to MediaCatch Vision API
        file_id = upload(self.file_path, self.type, extra=extra)

        # Wait for result
        result = wait_for_result(file_id)
        if not result:
            logger.error('Failed to get result from MediaCatch Vision API')
            return

        logger.info('Results:')
        pprint(result)

        # Save result to a file
        if self.save_result:
            Path(self.save_result).write_text(json.dumps(result, indent=4))
            logger.info(f'Result saved to {self.save_result}')
