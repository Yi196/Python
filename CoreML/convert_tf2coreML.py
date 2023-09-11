import coremltools as ct

# change tensorflow model to Core ML model
# mlmodel = ct.convert('../weights/movenet_singlepose_thunder_4', source='tensorflow',
#                     inputs=[ct.TensorType(shape=(1, 256, 256, 3))])
#
# cml_model_path = '../weights/movenet_singlepose.mlmodel'


mlmodel = ct.convert('../weights/movenet_multipose_lightning_1', source='tensorflow',
                    inputs=[ct.TensorType(shape=(1, 416, 416, 3))])

cml_model_path = '../weights/movenet_multipose.mlmodel'

mlmodel.save(cml_model_path)
print(mlmodel)