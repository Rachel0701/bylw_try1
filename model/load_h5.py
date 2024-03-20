from keras.models import load_model
import os
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

model = load_model('field_distinguish_model.h5')