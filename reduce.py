import FileHandler
from autoencoder import Autoencoder
from sklearn.model_selection import train_test_split

#Get arguments from command line
dataset,query,output_dataset,output_query = FileHandler.HandleArguments()

#Get dataframes from the input and query files
train_array = FileHandler.ReadInput(dataset)
print(len(train_array))


query_df = FileHandler.ReadInput(query,True)

#Split the data in training and validation
X_train,X_Val = train_test_split(train_array,test_size=0.2,random_state=42)

#todo:
#Initialize Neural Network
#Train Neural Network
#Tune Neural Network

model = Autoencoder()
model.train(X_train,X_Val)
model.evaluate(X_Val)




