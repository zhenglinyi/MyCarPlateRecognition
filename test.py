import CarplateInterface
import skimage.io as io

model,model_char = CarplateInterface.initialize()

path=input()
img,carplatenum = CarplateInterface.identify(model, model_char, path)

io.imshow(img)
print(carplatenum)
