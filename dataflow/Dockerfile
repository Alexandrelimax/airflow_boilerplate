FROM apache/beam_python3.12_sdk:2.64.0

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]
