import logging
import logging.config
import os

import hydra
import torch
from dataset_constants import Loggers
from hydra.utils import get_original_cwd
from lightning_transformers.task.nlp.token_classification import \
    TokenClassificationTransformer
from dataset_utils import align_dataset_on_model_max_length
from logging_utils import get_loggers_callbacks, set_logging_dir
from omegaconf import DictConfig, OmegaConf
from pytorch_lightning import Trainer
from pytorch_lightning.strategies import DDPStrategy
from transformers import AutoTokenizer, pipeline

from custom_lightning_modules import SlicerTokenClassificationDataModule
from lightning_transformers.task.nlp.token_classification import (
    TokenClassificationDataModule, TokenClassificationTransformer)
from datasets import load_dataset
# from pytorch_lightning.strategies import DDPStra
from transformers import GPTJForCausalLM, AutoModelForCausalLM, AutoTokenizer
import torch

log = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])

def gptj(cfg: DictConfig) -> None:
    # model = GPTJForCausalLM.from_pretrained(
    #     "EleutherAI/gpt-j-6B", revision="float16", torch_dtype=torch.float16, low_cpu_mem_usage=True
    # )
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")

    prompt = (
        "In a shocking finding, scientists discovered a herd of unicorns living in a remote, "
        "previously unexplored valley, in the Andes Mountains. Even more surprising to the "
        "researchers was the fact that the unicorns spoke perfect English."
    )

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    gen_tokens = model.generate(
        input_ids,
        do_sample=True,
        temperature=0.9,
        max_length=100,
    )
    gen_text = tokenizer.batch_decode(gen_tokens)[0]


@hydra.main(version_base="1.2", config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    set_logging_dir(log_output_path=f"{cfg.batch.logging_dir}/{cfg.loggers.tensorboard.version}",
                    log_config_path=f"{get_original_cwd()}/{cfg.log_config_path}"
                    )
    log.info(f'\nConfig Params:\n{OmegaConf.to_yaml(cfg)}')
    gptj(cfg)

if __name__ == "__main__":
    main()