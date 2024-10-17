# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.10-slim 

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /app

# contains files larger than 10 MiB.
COPY --chown=user ./projects/ex_sample /app/projects/ex_sample

# if you want new tutorial, can download with one command. 
# RUN python sample_dataset/eli5/load_eli5_dataset.py --save_path /app/projects/tutorial_1

# AutoRAG 실행 명령어를 CMD로 변경 eval <------
CMD ["autorag", "evaluate", "--config", "./projects/ex_sample/config.yaml", "--qa_data_path", "./projects/ex_sample/qa.parquet", "--corpus_data_path", "./projects/ex_sample/corpus.parquet"]
