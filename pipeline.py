import kfp
from kfp import dsl

def echo_op(text):
    return dsl.ContainerOp(
        name='echo',
        image='library/bash:4.4.23',
        command=['sh', '-c'],
        arguments=['echo %s' % text],
    )

@dsl.pipeline(
    name='Simple Pipeline',
    description='A simple pipeline that echoes a message.'
)
def simple_pipeline(message: str):
    echo_op(message)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(simple_pipeline, 'simple_pipeline.yaml')
