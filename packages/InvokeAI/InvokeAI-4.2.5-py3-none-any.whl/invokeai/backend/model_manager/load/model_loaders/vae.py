# Copyright (c) 2024, Lincoln D. Stein and the InvokeAI Development Team
"""Class for VAE model loading in InvokeAI."""

from pathlib import Path
from typing import Optional

import torch
from omegaconf import DictConfig, OmegaConf
from safetensors.torch import load_file as safetensors_load_file

from invokeai.backend.model_manager import (
    AnyModelConfig,
    BaseModelType,
    ModelFormat,
    ModelType,
)
from invokeai.backend.model_manager.config import AnyModel, CheckpointConfigBase
from invokeai.backend.model_manager.convert_ckpt_to_diffusers import convert_ldm_vae_to_diffusers

from .. import ModelLoaderRegistry
from .generic_diffusers import GenericDiffusersLoader


@ModelLoaderRegistry.register(base=BaseModelType.Any, type=ModelType.VAE, format=ModelFormat.Diffusers)
@ModelLoaderRegistry.register(base=BaseModelType.Any, type=ModelType.VAE, format=ModelFormat.Checkpoint)
class VAELoader(GenericDiffusersLoader):
    """Class to load VAE models."""

    def _needs_conversion(self, config: AnyModelConfig, model_path: Path, dest_path: Path) -> bool:
        if not isinstance(config, CheckpointConfigBase):
            return False
        elif (
            dest_path.exists()
            and (dest_path / "config.json").stat().st_mtime >= (config.converted_at or 0.0)
            and (dest_path / "config.json").stat().st_mtime >= model_path.stat().st_mtime
        ):
            return False
        else:
            return True

    def _convert_model(self, config: AnyModelConfig, model_path: Path, output_path: Optional[Path] = None) -> AnyModel:
        assert isinstance(config, CheckpointConfigBase)
        config_file = self._app_config.legacy_conf_path / config.config_path

        if model_path.suffix == ".safetensors":
            checkpoint = safetensors_load_file(model_path, device="cpu")
        else:
            checkpoint = torch.load(model_path, map_location="cpu")

        # sometimes weights are hidden under "state_dict", and sometimes not
        if "state_dict" in checkpoint:
            checkpoint = checkpoint["state_dict"]

        ckpt_config = OmegaConf.load(config_file)
        assert isinstance(ckpt_config, DictConfig)
        self._logger.info(f"Converting {model_path} to diffusers format")
        vae_model = convert_ldm_vae_to_diffusers(
            checkpoint=checkpoint,
            vae_config=ckpt_config,
            image_size=512,
            precision=self._torch_dtype,
            dump_path=output_path,
        )
        return vae_model
