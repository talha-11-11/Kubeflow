import kfp
from kfp import dsl
from kfp.components import create_component_from_func

# Define the preprocessing step
def preprocess_op():
    return dsl.ContainerOp(
        name='Preprocess Data',
        image='python:3.8',
        command=['sh', '-c'],
        arguments=[
            'pip install pandas scikit-learn && '
            'python -c "import pandas as pd; from sklearn.model_selection import train_test_split; '
            'data = pd.DataFrame({\'x\': range(100), \'y\': [i*2 for i in range(100)]}); '
            'train, test = train_test_split(data, test_size=0.2); '
            'train.to_csv(\'/train.csv\', index=False); test.to_csv(\'/test.csv\', index=False)"'
        ],
        file_outputs={
            'train': '/train.csv',
            'test': '/test.csv'
        }
    )

# Define the training step
def train_op(train_data):
    return dsl.ContainerOp(
        name='Train Model',
        image='python:3.8',
        command=['sh', '-c'],
        arguments=[
            'pip install pandas scikit-learn && '
            'python -c "import pandas as pd; from sklearn.linear_model import LinearRegression; '
            'train = pd.read_csv(\'%s\'); '
            'model = LinearRegression(); model.fit(train[[\'x\']], train[\'y\']); '
            'import joblib; joblib.dump(model, \'/model.joblib\')"' % train_data
        ],
        file_outputs={
            'model': '/model.joblib'
        }
    )

# Define the evaluation step
def evaluate_op(test_data, model):
    return dsl.ContainerOp(
        name='Evaluate Model',
        image='python:3.8',
        command=['sh', '-c'],
        arguments=[
            'pip install pandas scikit-learn joblib && '
            'python -c "import pandas as pd; from sklearn.linear_model import LinearRegression; '
            'from sklearn.metrics import mean_squared_error; import joblib; '
            'test = pd.read_csv(\'%s\'); model = joblib.load(\'%s\'); '
            'predictions = model.predict(test[[\'x\']]); '
            'mse = mean_squared_error(test[\'y\'], predictions); print(\'MSE: %s\' % mse)"' % (test_data, model)
        ]
    )

@dsl.pipeline(
    name='Enhanced Pipeline',
    description='An enhanced pipeline that includes data preprocessing, training, and evaluation.'
)
def enhanced_pipeline():
    preprocess = preprocess_op()
    train = train_op(preprocess.outputs['train'])
    evaluate = evaluate_op(preprocess.outputs['test'], train.outputs['model'])

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(enhanced_pipeline, 'enhanced_pipeline.yaml')
