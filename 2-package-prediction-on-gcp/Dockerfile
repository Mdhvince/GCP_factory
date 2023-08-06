FROM pytorch/torchserve:latest-cpu

WORKDIR /

COPY model-server /model-server

# Create torchserve config file (0.0.0.0 to run prediction on public IP)
USER root
RUN printf "\nservice_envelope=json" >> /model-server/config.properties
RUN printf "\ninference_address=http://0.0.0.0:7080" >> /model-server/config.properties
RUN printf "\nmanagement_address=http://0.0.0.0:7081" >> /model-server/config.properties
USER model-server

# Expose health and prediction listener ports from the image
EXPOSE 7080
EXPOSE 7081

# create an APP_NAME variable
ENV APP_NAME=myapp

# Create the model archive file that packages the entire model-server directory. Example for Scripted Model
# Export the resulting .mar file to the model-store directory
RUN torch-model-archiver \
    --model-name=$APP_NAME \
    --version=1.0  \
    --serialized-file=/model-server/ts_model.pt  \
    --extra-files=/model-server/index_to_name.json  \
    --handler=/model-server/model_handler_online_prediction.py \
    --export-path=/model-server/model-store

# Run torchserve http server. This wrap Pytorch model into a REST API
CMD ["torchserve", \
     "--start", \
     "--model-store", "/model-server/model-store", \
     "--models", "$APP_NAME=$APP_NAME.mar", \
     "--ts-config", "/model-server/config.properties"]


