FROM python:3.8
ENV DASH_DEBUG_MODE true
COPY ./segmentation_app /segmentation_app
COPY requirements.txt segmentation_app/requirements.txt
WORKDIR /segmentation_app
RUN set -ex && \
    pip install -r requirements.txt
RUN python efood_analysis.py
EXPOSE 8050 80 8080
CMD ["python", "index.py"]