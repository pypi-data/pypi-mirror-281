r'''
# CDK Arch

This library aims at providing a way to autogenerate architectural diagrams for CDK projects.

This library is  written using the wonderful [projen](https://github.com/projen/projen) framework.

# Installation

The library is available on npmjs.com and can be installed using:

`npm i cdk-arch`

And on pypi:

`pip install cdk-arch`

# Usage Examples

As an example, let's consider the following CDK app:

```python
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export class ExampleStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'Bucket');
    const lfunction = new lambda.Function(this, 'Lambda', {
        ...
    });
  }
}

const app = new cdk.App();
new ExampleStack(app, 'ExampleStack', {
env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'eu-west-1',
},
});
```

and imagine that in the diagram we want to show the bucket, the lambda function and an arrow connecting the two.
This can be accomplished by changing the code as follows:

```python
export class ExampleStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'Bucket');
    const lfunction = new lambda.Function(this, 'Lambda', {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async function(event) {
          console.log('event', event);
          return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Hello from Lambda!' }),
          };
        };
      `),
      environment: {
        BUCKET_NAME: bucket.bucketName,
      },
    });

    // We add some metadata to the resources to be able to position them in the diagram
    bucket.node.addMetadata('CDKArch Element', { x: 0, y: 0 });
    lfunction.node.addMetadata('CDKArch Element', { x: 300, y: 0 });
    // We add a connection between the bucket and the lambda function
    bucket.node.addMetadata('CDKArch Connection', { startId: bucket.node.id, endId: lfunction.node.id });

  }
}

const app = new cdk.App();
new ExampleStack(app, 'ExampleStack', {
    env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'eu-west-1',
    },
});

const sketchbuilder = new SketchBuilder();
Aspects.of(app).add(sketchbuilder);

app.synth();
sketchbuilder.exportToFile(filepath);
```

where we added some metadata to the resources to instruct the SketchBuilder to position two icons in the diagram and a connection between the two,
and we added an aspect to the app to instruct the SketchBuilder to generate it when the app is synthetized.

This is the resulting diagram:

![Example Diagram](./examples/example/example.png)

### Customizing the diagram

#### Positioning the resources

The position of the resources in the diagram can be customized using the 'x' and 'y' fields in the metadata of the node:

```python
bucket.node.addMetadata('CDKArch Element', { x: 100, y: 200 });
```

#### Name of the resouces

By default, the name of the resources is the id of the node. This can be customized by adding a 'text' field to the metadata of the node:

```python
bucket.node.addMetadata('CDKArch Element', { x: 100, y: 200, text: 'Overriding the bucket name' });
```

# Contributors

Matteo Giani [matteo.giani.87@gmail.com](mailto:matteo.giani.87@gmail.com)
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-arch.AppState",
    jsii_struct_bases=[],
    name_mapping={
        "grid_size": "gridSize",
        "view_background_color": "viewBackgroundColor",
    },
)
class AppState:
    def __init__(
        self,
        *,
        grid_size: typing.Any,
        view_background_color: builtins.str,
    ) -> None:
        '''
        :param grid_size: 
        :param view_background_color: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1b5a072db5320165d1c6b06de8faebc55825227b01c089757ce9afbc274fe5)
            check_type(argname="argument grid_size", value=grid_size, expected_type=type_hints["grid_size"])
            check_type(argname="argument view_background_color", value=view_background_color, expected_type=type_hints["view_background_color"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "grid_size": grid_size,
            "view_background_color": view_background_color,
        }

    @builtins.property
    def grid_size(self) -> typing.Any:
        result = self._values.get("grid_size")
        assert result is not None, "Required property 'grid_size' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def view_background_color(self) -> builtins.str:
        result = self._values.get("view_background_color")
        assert result is not None, "Required property 'view_background_color' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-arch.ArrowHead")
class ArrowHead(enum.Enum):
    TRIANGLE = "TRIANGLE"
    ARROW = "ARROW"


@jsii.data_type(
    jsii_type="cdk-arch.Binding",
    jsii_struct_bases=[],
    name_mapping={"element_id": "elementId", "focus": "focus", "gap": "gap"},
)
class Binding:
    def __init__(
        self,
        *,
        element_id: builtins.str,
        focus: jsii.Number,
        gap: jsii.Number,
    ) -> None:
        '''
        :param element_id: 
        :param focus: 
        :param gap: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54af41b23d2df745b9acbab7ed8c3f8cb5bd6fa1e2a61ff87e36487c8c88f6b)
            check_type(argname="argument element_id", value=element_id, expected_type=type_hints["element_id"])
            check_type(argname="argument focus", value=focus, expected_type=type_hints["focus"])
            check_type(argname="argument gap", value=gap, expected_type=type_hints["gap"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "element_id": element_id,
            "focus": focus,
            "gap": gap,
        }

    @builtins.property
    def element_id(self) -> builtins.str:
        result = self._values.get("element_id")
        assert result is not None, "Required property 'element_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def focus(self) -> jsii.Number:
        result = self._values.get("focus")
        assert result is not None, "Required property 'focus' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def gap(self) -> jsii.Number:
        result = self._values.get("gap")
        assert result is not None, "Required property 'gap' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Binding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-arch.BoundElement",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "type": "type"},
)
class BoundElement:
    def __init__(self, *, id: builtins.str, type: builtins.str) -> None:
        '''
        :param id: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6754c85b8d47ae016d1e5f0ead6f596a886914e8af2cca7147db03050e016c3)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "type": type,
        }

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BoundElement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExcaliDrawPrimitive(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-arch.ExcaliDrawPrimitive",
):
    def __init__(
        self,
        *,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        '''
        args = ExcaliDrawPrimitiveProps(
            group_ids=group_ids, height=height, type=type, width=width, x=x, y=y
        )

        jsii.create(self.__class__, self, [args])

    @jsii.member(jsii_name="addBoundElement")
    def add_bound_element(self, element: "ExcaliDrawPrimitive") -> None:
        '''
        :param element: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d7d7e2a37ff5a6a34fd6c14c450597ae7b490fee4ae49215abf41555107aff)
            check_type(argname="argument element", value=element, expected_type=type_hints["element"])
        return typing.cast(None, jsii.invoke(self, "addBoundElement", [element]))

    @builtins.property
    @jsii.member(jsii_name="angle")
    def angle(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "angle"))

    @angle.setter
    def angle(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c189f02e5d5f92cbea9eb55ca318d8fd0b7c72ed5d7988dd483b4e0afb0adea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "angle", value)

    @builtins.property
    @jsii.member(jsii_name="boundElements")
    def bound_elements(self) -> typing.List[BoundElement]:
        return typing.cast(typing.List[BoundElement], jsii.get(self, "boundElements"))

    @bound_elements.setter
    def bound_elements(self, value: typing.List[BoundElement]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f111879e8cc5b64c8d18bd5c0922a702a517042d91b44860ff9e92b4430014e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "boundElements", value)

    @builtins.property
    @jsii.member(jsii_name="frameId")
    def frame_id(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "frameId"))

    @frame_id.setter
    def frame_id(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93f44f7a4f655147d77f804918dfee0f51bdc5f3d1d854ad000fe737c1c6ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frameId", value)

    @builtins.property
    @jsii.member(jsii_name="groupIds")
    def group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupIds"))

    @group_ids.setter
    def group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3fa03235d0cc13a57a6a81c164ade8dfd4b77415f149fa10c52112ef9e34dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIds", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d2893fd63642dc63478281c5f8786e30a2f0b93327d659107235cfb0b889ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db800d0773b1c17c437bb0338fa3f235e608ed0fe11a5581eff05673b742fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isDeleted")
    def is_deleted(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isDeleted"))

    @is_deleted.setter
    def is_deleted(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83ab6be018dca84f96bbf5bae6d58630ddda66a0fa9e794bf57c141e5fd4bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDeleted", value)

    @builtins.property
    @jsii.member(jsii_name="link")
    def link(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "link"))

    @link.setter
    def link(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1800345b4e65c2df95fe80e43e2405dc7834b4733b2ebfc348190434131ed5ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "link", value)

    @builtins.property
    @jsii.member(jsii_name="locked")
    def locked(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "locked"))

    @locked.setter
    def locked(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfba71bf31fcd278dec4d42e22d46f875824e04cd5266c7dbfbc17a1a6c95e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locked", value)

    @builtins.property
    @jsii.member(jsii_name="seed")
    def seed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seed"))

    @seed.setter
    def seed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a86911b993700ce3b247fd41b3c205f66b7a6e1d4ec0541c8f0e338af048c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seed", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9597604abbde6d8bee00450844e06fb058c3aae95167ae363c740100f1d03596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "updated"))

    @updated.setter
    def updated(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63cba1d3f51dfaa539695db9455a8d6d4afaa959ff5c697e43dd983a1796748a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updated", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @version.setter
    def version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6090be5c4eb7c96f523f85d31e5905f730d689074c6f3e051cfb88b90332fcc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="versionNonce")
    def version_nonce(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "versionNonce"))

    @version_nonce.setter
    def version_nonce(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb25aacf45ba92f11e3bad14a82dfc8ea23c0a1bd6f2a0dd4140ba5918878ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionNonce", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef06167fb2a721ff4b4b265c531c7c698660040727f40fa9e44b842bcbda454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="x")
    def x(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "x"))

    @x.setter
    def x(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3040e9bc92098a365cefeade34ca2ac50892c720b22babb511e30aba46a113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x", value)

    @builtins.property
    @jsii.member(jsii_name="y")
    def y(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "y"))

    @y.setter
    def y(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b22b9037f7475e7e948f10644eebd95f28d2c462b73f67b82e49d645ccc799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "y", value)


class _ExcaliDrawPrimitiveProxy(ExcaliDrawPrimitive):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ExcaliDrawPrimitive).__jsii_proxy_class__ = lambda : _ExcaliDrawPrimitiveProxy


@jsii.data_type(
    jsii_type="cdk-arch.ExcaliDrawPrimitiveProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_ids": "groupIds",
        "height": "height",
        "type": "type",
        "width": "width",
        "x": "x",
        "y": "y",
    },
)
class ExcaliDrawPrimitiveProps:
    def __init__(
        self,
        *,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee22f3a6f3f27673bcd2e04e25daf3880763678f6bb42c25e675badfcdd9c3bc)
            check_type(argname="argument group_ids", value=group_ids, expected_type=type_hints["group_ids"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_ids is not None:
            self._values["group_ids"] = group_ids
        if height is not None:
            self._values["height"] = height
        if type is not None:
            self._values["type"] = type
        if width is not None:
            self._values["width"] = width
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y

    @builtins.property
    def group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExcaliDrawPrimitiveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-arch.FillStyle")
class FillStyle(enum.Enum):
    HACHURE = "HACHURE"
    SOLID = "SOLID"
    CROSSHATCH = "CROSSHATCH"
    DOTS = "DOTS"


class Icon(metaclass=jsii.JSIIMeta, jsii_type="cdk-arch.Icon"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromConstruct")
    @builtins.classmethod
    def from_construct(cls, node: _constructs_77d1e7e8.IConstruct) -> "Icon":
        '''
        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975f575bf69f5571570bd08f3b0c2ecde4dfc73d6a2f7e0b86d4f5396625825a)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("Icon", jsii.sinvoke(cls, "fromConstruct", [node]))

    @jsii.member(jsii_name="elements")
    def elements(self) -> typing.List[ExcaliDrawPrimitive]:
        return typing.cast(typing.List[ExcaliDrawPrimitive], jsii.invoke(self, "elements", []))

    @jsii.member(jsii_name="loadJsonIcon")
    def load_json_icon(
        self,
        icon_file: builtins.str,
        node: _constructs_77d1e7e8.IConstruct,
    ) -> None:
        '''
        :param icon_file: -
        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1a57a529be3c82cfa1ab67d4ebaa2640eb0911bdbc6c0769b20775b471379a)
            check_type(argname="argument icon_file", value=icon_file, expected_type=type_hints["icon_file"])
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "loadJsonIcon", [icon_file, node]))

    @jsii.member(jsii_name="moveIcon")
    def move_icon(self, x: jsii.Number, y: jsii.Number) -> None:
        '''
        :param x: -
        :param y: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dea3c9521a816ab322412263464cd7323e491ccf3b862f977051de5d8a6f2a7)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        return typing.cast(None, jsii.invoke(self, "moveIcon", [x, y]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="iconPath")
    def ICON_PATH(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "iconPath"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="icons")
    def ICONS(cls) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.sget(cls, "icons"))

    @builtins.property
    @jsii.member(jsii_name="box")
    def box(self) -> "Rectangle":
        return typing.cast("Rectangle", jsii.get(self, "box"))

    @box.setter
    def box(self, value: "Rectangle") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7055f4625f379e0de775bad1836cef96c83d45cd83706560856ac15d00e60f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "box", value)

    @builtins.property
    @jsii.member(jsii_name="iconElements")
    def icon_elements(self) -> typing.List[ExcaliDrawPrimitive]:
        return typing.cast(typing.List[ExcaliDrawPrimitive], jsii.get(self, "iconElements"))

    @icon_elements.setter
    def icon_elements(self, value: typing.List[ExcaliDrawPrimitive]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8397895529458deb3ef5a6499cc99a28ad44f4a511b7b56b70f6b6528f337d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iconElements", value)

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> "Text":
        return typing.cast("Text", jsii.get(self, "text"))

    @text.setter
    def text(self, value: "Text") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc07c5e2cbc56a5a25da850c11d479f3712bcea4cef18ee6fc4ec431c10baadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value)


@jsii.data_type(
    jsii_type="cdk-arch.Roundness",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class Roundness:
    def __init__(self, *, type: jsii.Number) -> None:
        '''
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d8b8c44a6e92d896a292613905d455fe47b68e4d2b70c3ed95854f95a6bc15)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> jsii.Number:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Roundness(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SketchBuilder(metaclass=jsii.JSIIMeta, jsii_type="cdk-arch.SketchBuilder"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addArrow")
    def add_arrow(
        self,
        start_node_id: builtins.str,
        end_node_id: builtins.str,
    ) -> builtins.str:
        '''
        :param start_node_id: -
        :param end_node_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29830b4b892acf2e556bd163570ecc436a736c9f6dfe447324a2cc8f5fde87a)
            check_type(argname="argument start_node_id", value=start_node_id, expected_type=type_hints["start_node_id"])
            check_type(argname="argument end_node_id", value=end_node_id, expected_type=type_hints["end_node_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "addArrow", [start_node_id, end_node_id]))

    @jsii.member(jsii_name="addIconForConstruct")
    def add_icon_for_construct(
        self,
        node: _constructs_77d1e7e8.IConstruct,
        *,
        data: typing.Any,
        type: builtins.str,
        trace: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param node: -
        :param data: The data.
        :param type: The metadata entry type.
        :param trace: Stack trace at the point of adding the metadata. Only available if ``addMetadata()`` is called with ``stackTrace: true``. Default: - no trace information
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbaeb8ddf94148aa74f0dbc0ad9296d0ab99803dd1fc0f6ca5f1e8b6f7c3eef7)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        metadata = _constructs_77d1e7e8.MetadataEntry(
            data=data, type=type, trace=trace
        )

        return typing.cast(None, jsii.invoke(self, "addIconForConstruct", [node, metadata]))

    @jsii.member(jsii_name="exportToFile")
    def export_to_file(self, save_path: builtins.str) -> None:
        '''
        :param save_path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcdba1e318804db715fa5633c8f5bccf7d78acda7a2952d58d1e4d4216eedc06)
            check_type(argname="argument save_path", value=save_path, expected_type=type_hints["save_path"])
        return typing.cast(None, jsii.invoke(self, "exportToFile", [save_path]))

    @jsii.member(jsii_name="registerArrow")
    def register_arrow(
        self,
        start_node_id: builtins.str,
        end_node_id: builtins.str,
    ) -> None:
        '''
        :param start_node_id: -
        :param end_node_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb4fe00223b05d5aa286bca9debfa08e09ba6aeaa52344db48af0dabe146960)
            check_type(argname="argument start_node_id", value=start_node_id, expected_type=type_hints["start_node_id"])
            check_type(argname="argument end_node_id", value=end_node_id, expected_type=type_hints["end_node_id"])
        return typing.cast(None, jsii.invoke(self, "registerArrow", [start_node_id, end_node_id]))

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''
        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a27775148d320656bb0b61d5dc8bb785f2ec5357bcf45e9c2bb28763a87e99)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

    @builtins.property
    @jsii.member(jsii_name="arrowIconGap")
    def arrow_icon_gap(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "arrowIconGap"))

    @arrow_icon_gap.setter
    def arrow_icon_gap(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30c62e2bba773276c31f578d188ef1b8e74d1789437adb3b9be9e59d45bcc79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrowIconGap", value)

    @builtins.property
    @jsii.member(jsii_name="arrows")
    def arrows(self) -> typing.List["Arrow"]:
        return typing.cast(typing.List["Arrow"], jsii.get(self, "arrows"))

    @arrows.setter
    def arrows(self, value: typing.List["Arrow"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09d5766d1564ab796d7c6ce26dbcb5e83a09705db378ce48b0beef83e4fdca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrows", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429cde3a253b2e03ed91c1925bc222937b12f27eee48f17f3dd955ad2837ffa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="icons")
    def icons(self) -> typing.Mapping[builtins.str, Icon]:
        return typing.cast(typing.Mapping[builtins.str, Icon], jsii.get(self, "icons"))

    @icons.setter
    def icons(self, value: typing.Mapping[builtins.str, Icon]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b139745652812d01e8d0a06fa0b2fd88fb461219e6b114be51a61f441a1d394c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icons", value)


@jsii.enum(jsii_type="cdk-arch.StrokeStyle")
class StrokeStyle(enum.Enum):
    SOLID = "SOLID"
    DASHED = "DASHED"
    DOTTED = "DOTTED"


@jsii.enum(jsii_type="cdk-arch.TextAlign")
class TextAlign(enum.Enum):
    CENTER = "CENTER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@jsii.enum(jsii_type="cdk-arch.VerticalAlign")
class VerticalAlign(enum.Enum):
    TOP = "TOP"


class DrawnObject(
    ExcaliDrawPrimitive,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-arch.DrawnObject",
):
    def __init__(
        self,
        *,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        '''
        args = DrawnObjectProps(
            background_color=background_color,
            fill_style=fill_style,
            opacity=opacity,
            roughness=roughness,
            roundness=roundness,
            stroke_color=stroke_color,
            stroke_style=stroke_style,
            stroke_width=stroke_width,
            group_ids=group_ids,
            height=height,
            type=type,
            width=width,
            x=x,
            y=y,
        )

        jsii.create(self.__class__, self, [args])

    @builtins.property
    @jsii.member(jsii_name="backgroundColor")
    def background_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backgroundColor"))

    @builtins.property
    @jsii.member(jsii_name="fillStyle")
    def fill_style(self) -> FillStyle:
        return typing.cast(FillStyle, jsii.get(self, "fillStyle"))

    @builtins.property
    @jsii.member(jsii_name="opacity")
    def opacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "opacity"))

    @builtins.property
    @jsii.member(jsii_name="roughness")
    def roughness(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "roughness"))

    @builtins.property
    @jsii.member(jsii_name="roundness")
    def roundness(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "roundness"))

    @builtins.property
    @jsii.member(jsii_name="strokeColor")
    def stroke_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "strokeColor"))

    @builtins.property
    @jsii.member(jsii_name="strokeStyle")
    def stroke_style(self) -> StrokeStyle:
        return typing.cast(StrokeStyle, jsii.get(self, "strokeStyle"))

    @builtins.property
    @jsii.member(jsii_name="strokeWidth")
    def stroke_width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "strokeWidth"))


class _DrawnObjectProxy(
    DrawnObject,
    jsii.proxy_for(ExcaliDrawPrimitive), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DrawnObject).__jsii_proxy_class__ = lambda : _DrawnObjectProxy


@jsii.data_type(
    jsii_type="cdk-arch.DrawnObjectProps",
    jsii_struct_bases=[ExcaliDrawPrimitiveProps],
    name_mapping={
        "group_ids": "groupIds",
        "height": "height",
        "type": "type",
        "width": "width",
        "x": "x",
        "y": "y",
        "background_color": "backgroundColor",
        "fill_style": "fillStyle",
        "opacity": "opacity",
        "roughness": "roughness",
        "roundness": "roundness",
        "stroke_color": "strokeColor",
        "stroke_style": "strokeStyle",
        "stroke_width": "strokeWidth",
    },
)
class DrawnObjectProps(ExcaliDrawPrimitiveProps):
    def __init__(
        self,
        *,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ccd3bf03f8618e77520f79389281e9253317c4aeff026d46c273e80ad029112)
            check_type(argname="argument group_ids", value=group_ids, expected_type=type_hints["group_ids"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
            check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
            check_type(argname="argument fill_style", value=fill_style, expected_type=type_hints["fill_style"])
            check_type(argname="argument opacity", value=opacity, expected_type=type_hints["opacity"])
            check_type(argname="argument roughness", value=roughness, expected_type=type_hints["roughness"])
            check_type(argname="argument roundness", value=roundness, expected_type=type_hints["roundness"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument stroke_style", value=stroke_style, expected_type=type_hints["stroke_style"])
            check_type(argname="argument stroke_width", value=stroke_width, expected_type=type_hints["stroke_width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_ids is not None:
            self._values["group_ids"] = group_ids
        if height is not None:
            self._values["height"] = height
        if type is not None:
            self._values["type"] = type
        if width is not None:
            self._values["width"] = width
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y
        if background_color is not None:
            self._values["background_color"] = background_color
        if fill_style is not None:
            self._values["fill_style"] = fill_style
        if opacity is not None:
            self._values["opacity"] = opacity
        if roughness is not None:
            self._values["roughness"] = roughness
        if roundness is not None:
            self._values["roundness"] = roundness
        if stroke_color is not None:
            self._values["stroke_color"] = stroke_color
        if stroke_style is not None:
            self._values["stroke_style"] = stroke_style
        if stroke_width is not None:
            self._values["stroke_width"] = stroke_width

    @builtins.property
    def group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def background_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fill_style(self) -> typing.Optional[FillStyle]:
        result = self._values.get("fill_style")
        return typing.cast(typing.Optional[FillStyle], result)

    @builtins.property
    def opacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("opacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roughness(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("roughness")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roundness(self) -> typing.Any:
        result = self._values.get("roundness")
        return typing.cast(typing.Any, result)

    @builtins.property
    def stroke_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stroke_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stroke_style(self) -> typing.Optional[StrokeStyle]:
        result = self._values.get("stroke_style")
        return typing.cast(typing.Optional[StrokeStyle], result)

    @builtins.property
    def stroke_width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("stroke_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DrawnObjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ellipse(DrawnObject, metaclass=jsii.JSIIMeta, jsii_type="cdk-arch.Ellipse"):
    def __init__(
        self,
        *,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        '''
        args = EllipseProps(
            end_arrowhead=end_arrowhead,
            end_binding=end_binding,
            last_committed_point=last_committed_point,
            start_arrowhead=start_arrowhead,
            start_binding=start_binding,
            background_color=background_color,
            fill_style=fill_style,
            opacity=opacity,
            roughness=roughness,
            roundness=roundness,
            stroke_color=stroke_color,
            stroke_style=stroke_style,
            stroke_width=stroke_width,
            group_ids=group_ids,
            height=height,
            type=type,
            width=width,
            x=x,
            y=y,
        )

        jsii.create(self.__class__, self, [args])


class LineLike(
    DrawnObject,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-arch.LineLike",
):
    def __init__(
        self,
        *,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        '''
        args = LineLikeProps(
            end_arrowhead=end_arrowhead,
            end_binding=end_binding,
            last_committed_point=last_committed_point,
            start_arrowhead=start_arrowhead,
            start_binding=start_binding,
            background_color=background_color,
            fill_style=fill_style,
            opacity=opacity,
            roughness=roughness,
            roundness=roundness,
            stroke_color=stroke_color,
            stroke_style=stroke_style,
            stroke_width=stroke_width,
            group_ids=group_ids,
            height=height,
            type=type,
            width=width,
            x=x,
            y=y,
        )

        jsii.create(self.__class__, self, [args])

    @builtins.property
    @jsii.member(jsii_name="endArrowhead")
    def end_arrowhead(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "endArrowhead"))

    @builtins.property
    @jsii.member(jsii_name="endBinding")
    def end_binding(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "endBinding"))

    @builtins.property
    @jsii.member(jsii_name="lastCommittedPoint")
    def last_committed_point(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "lastCommittedPoint"))

    @builtins.property
    @jsii.member(jsii_name="startArrowhead")
    def start_arrowhead(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "startArrowhead"))

    @builtins.property
    @jsii.member(jsii_name="startBinding")
    def start_binding(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "startBinding"))


class _LineLikeProxy(
    LineLike,
    jsii.proxy_for(DrawnObject), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, LineLike).__jsii_proxy_class__ = lambda : _LineLikeProxy


@jsii.data_type(
    jsii_type="cdk-arch.LineLikeProps",
    jsii_struct_bases=[DrawnObjectProps],
    name_mapping={
        "group_ids": "groupIds",
        "height": "height",
        "type": "type",
        "width": "width",
        "x": "x",
        "y": "y",
        "background_color": "backgroundColor",
        "fill_style": "fillStyle",
        "opacity": "opacity",
        "roughness": "roughness",
        "roundness": "roundness",
        "stroke_color": "strokeColor",
        "stroke_style": "strokeStyle",
        "stroke_width": "strokeWidth",
        "end_arrowhead": "endArrowhead",
        "end_binding": "endBinding",
        "last_committed_point": "lastCommittedPoint",
        "start_arrowhead": "startArrowhead",
        "start_binding": "startBinding",
    },
)
class LineLikeProps(DrawnObjectProps):
    def __init__(
        self,
        *,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
    ) -> None:
        '''
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8440156e2fba197d0bf38a2beb21c0bbb07cb3c4352bbfd92e0de87dc6fb6a)
            check_type(argname="argument group_ids", value=group_ids, expected_type=type_hints["group_ids"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
            check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
            check_type(argname="argument fill_style", value=fill_style, expected_type=type_hints["fill_style"])
            check_type(argname="argument opacity", value=opacity, expected_type=type_hints["opacity"])
            check_type(argname="argument roughness", value=roughness, expected_type=type_hints["roughness"])
            check_type(argname="argument roundness", value=roundness, expected_type=type_hints["roundness"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument stroke_style", value=stroke_style, expected_type=type_hints["stroke_style"])
            check_type(argname="argument stroke_width", value=stroke_width, expected_type=type_hints["stroke_width"])
            check_type(argname="argument end_arrowhead", value=end_arrowhead, expected_type=type_hints["end_arrowhead"])
            check_type(argname="argument end_binding", value=end_binding, expected_type=type_hints["end_binding"])
            check_type(argname="argument last_committed_point", value=last_committed_point, expected_type=type_hints["last_committed_point"])
            check_type(argname="argument start_arrowhead", value=start_arrowhead, expected_type=type_hints["start_arrowhead"])
            check_type(argname="argument start_binding", value=start_binding, expected_type=type_hints["start_binding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_ids is not None:
            self._values["group_ids"] = group_ids
        if height is not None:
            self._values["height"] = height
        if type is not None:
            self._values["type"] = type
        if width is not None:
            self._values["width"] = width
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y
        if background_color is not None:
            self._values["background_color"] = background_color
        if fill_style is not None:
            self._values["fill_style"] = fill_style
        if opacity is not None:
            self._values["opacity"] = opacity
        if roughness is not None:
            self._values["roughness"] = roughness
        if roundness is not None:
            self._values["roundness"] = roundness
        if stroke_color is not None:
            self._values["stroke_color"] = stroke_color
        if stroke_style is not None:
            self._values["stroke_style"] = stroke_style
        if stroke_width is not None:
            self._values["stroke_width"] = stroke_width
        if end_arrowhead is not None:
            self._values["end_arrowhead"] = end_arrowhead
        if end_binding is not None:
            self._values["end_binding"] = end_binding
        if last_committed_point is not None:
            self._values["last_committed_point"] = last_committed_point
        if start_arrowhead is not None:
            self._values["start_arrowhead"] = start_arrowhead
        if start_binding is not None:
            self._values["start_binding"] = start_binding

    @builtins.property
    def group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def background_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fill_style(self) -> typing.Optional[FillStyle]:
        result = self._values.get("fill_style")
        return typing.cast(typing.Optional[FillStyle], result)

    @builtins.property
    def opacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("opacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roughness(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("roughness")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roundness(self) -> typing.Any:
        result = self._values.get("roundness")
        return typing.cast(typing.Any, result)

    @builtins.property
    def stroke_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stroke_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stroke_style(self) -> typing.Optional[StrokeStyle]:
        result = self._values.get("stroke_style")
        return typing.cast(typing.Optional[StrokeStyle], result)

    @builtins.property
    def stroke_width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("stroke_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_arrowhead(self) -> typing.Any:
        result = self._values.get("end_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def end_binding(self) -> typing.Any:
        result = self._values.get("end_binding")
        return typing.cast(typing.Any, result)

    @builtins.property
    def last_committed_point(self) -> typing.Any:
        result = self._values.get("last_committed_point")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_arrowhead(self) -> typing.Any:
        result = self._values.get("start_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_binding(self) -> typing.Any:
        result = self._values.get("start_binding")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LineLikeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-arch.LineProps",
    jsii_struct_bases=[LineLikeProps],
    name_mapping={
        "group_ids": "groupIds",
        "height": "height",
        "type": "type",
        "width": "width",
        "x": "x",
        "y": "y",
        "background_color": "backgroundColor",
        "fill_style": "fillStyle",
        "opacity": "opacity",
        "roughness": "roughness",
        "roundness": "roundness",
        "stroke_color": "strokeColor",
        "stroke_style": "strokeStyle",
        "stroke_width": "strokeWidth",
        "end_arrowhead": "endArrowhead",
        "end_binding": "endBinding",
        "last_committed_point": "lastCommittedPoint",
        "start_arrowhead": "startArrowhead",
        "start_binding": "startBinding",
        "points": "points",
    },
)
class LineProps(LineLikeProps):
    def __init__(
        self,
        *,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
        points: typing.Optional[typing.Sequence[typing.Sequence[jsii.Number]]] = None,
    ) -> None:
        '''
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        :param points: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d922aed9ee428fe5eab84a1b2311230bd05063663d106cbd9a62ae3a3b9b21)
            check_type(argname="argument group_ids", value=group_ids, expected_type=type_hints["group_ids"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
            check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
            check_type(argname="argument fill_style", value=fill_style, expected_type=type_hints["fill_style"])
            check_type(argname="argument opacity", value=opacity, expected_type=type_hints["opacity"])
            check_type(argname="argument roughness", value=roughness, expected_type=type_hints["roughness"])
            check_type(argname="argument roundness", value=roundness, expected_type=type_hints["roundness"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument stroke_style", value=stroke_style, expected_type=type_hints["stroke_style"])
            check_type(argname="argument stroke_width", value=stroke_width, expected_type=type_hints["stroke_width"])
            check_type(argname="argument end_arrowhead", value=end_arrowhead, expected_type=type_hints["end_arrowhead"])
            check_type(argname="argument end_binding", value=end_binding, expected_type=type_hints["end_binding"])
            check_type(argname="argument last_committed_point", value=last_committed_point, expected_type=type_hints["last_committed_point"])
            check_type(argname="argument start_arrowhead", value=start_arrowhead, expected_type=type_hints["start_arrowhead"])
            check_type(argname="argument start_binding", value=start_binding, expected_type=type_hints["start_binding"])
            check_type(argname="argument points", value=points, expected_type=type_hints["points"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_ids is not None:
            self._values["group_ids"] = group_ids
        if height is not None:
            self._values["height"] = height
        if type is not None:
            self._values["type"] = type
        if width is not None:
            self._values["width"] = width
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y
        if background_color is not None:
            self._values["background_color"] = background_color
        if fill_style is not None:
            self._values["fill_style"] = fill_style
        if opacity is not None:
            self._values["opacity"] = opacity
        if roughness is not None:
            self._values["roughness"] = roughness
        if roundness is not None:
            self._values["roundness"] = roundness
        if stroke_color is not None:
            self._values["stroke_color"] = stroke_color
        if stroke_style is not None:
            self._values["stroke_style"] = stroke_style
        if stroke_width is not None:
            self._values["stroke_width"] = stroke_width
        if end_arrowhead is not None:
            self._values["end_arrowhead"] = end_arrowhead
        if end_binding is not None:
            self._values["end_binding"] = end_binding
        if last_committed_point is not None:
            self._values["last_committed_point"] = last_committed_point
        if start_arrowhead is not None:
            self._values["start_arrowhead"] = start_arrowhead
        if start_binding is not None:
            self._values["start_binding"] = start_binding
        if points is not None:
            self._values["points"] = points

    @builtins.property
    def group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def background_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fill_style(self) -> typing.Optional[FillStyle]:
        result = self._values.get("fill_style")
        return typing.cast(typing.Optional[FillStyle], result)

    @builtins.property
    def opacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("opacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roughness(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("roughness")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roundness(self) -> typing.Any:
        result = self._values.get("roundness")
        return typing.cast(typing.Any, result)

    @builtins.property
    def stroke_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stroke_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stroke_style(self) -> typing.Optional[StrokeStyle]:
        result = self._values.get("stroke_style")
        return typing.cast(typing.Optional[StrokeStyle], result)

    @builtins.property
    def stroke_width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("stroke_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_arrowhead(self) -> typing.Any:
        result = self._values.get("end_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def end_binding(self) -> typing.Any:
        result = self._values.get("end_binding")
        return typing.cast(typing.Any, result)

    @builtins.property
    def last_committed_point(self) -> typing.Any:
        result = self._values.get("last_committed_point")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_arrowhead(self) -> typing.Any:
        result = self._values.get("start_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_binding(self) -> typing.Any:
        result = self._values.get("start_binding")
        return typing.cast(typing.Any, result)

    @builtins.property
    def points(self) -> typing.Optional[typing.List[typing.List[jsii.Number]]]:
        result = self._values.get("points")
        return typing.cast(typing.Optional[typing.List[typing.List[jsii.Number]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Rectangle(DrawnObject, metaclass=jsii.JSIIMeta, jsii_type="cdk-arch.Rectangle"):
    def __init__(
        self,
        *,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        '''
        args = LineLikeProps(
            end_arrowhead=end_arrowhead,
            end_binding=end_binding,
            last_committed_point=last_committed_point,
            start_arrowhead=start_arrowhead,
            start_binding=start_binding,
            background_color=background_color,
            fill_style=fill_style,
            opacity=opacity,
            roughness=roughness,
            roundness=roundness,
            stroke_color=stroke_color,
            stroke_style=stroke_style,
            stroke_width=stroke_width,
            group_ids=group_ids,
            height=height,
            type=type,
            width=width,
            x=x,
            y=y,
        )

        jsii.create(self.__class__, self, [args])


@jsii.data_type(
    jsii_type="cdk-arch.RectangleProps",
    jsii_struct_bases=[LineLikeProps],
    name_mapping={
        "group_ids": "groupIds",
        "height": "height",
        "type": "type",
        "width": "width",
        "x": "x",
        "y": "y",
        "background_color": "backgroundColor",
        "fill_style": "fillStyle",
        "opacity": "opacity",
        "roughness": "roughness",
        "roundness": "roundness",
        "stroke_color": "strokeColor",
        "stroke_style": "strokeStyle",
        "stroke_width": "strokeWidth",
        "end_arrowhead": "endArrowhead",
        "end_binding": "endBinding",
        "last_committed_point": "lastCommittedPoint",
        "start_arrowhead": "startArrowhead",
        "start_binding": "startBinding",
    },
)
class RectangleProps(LineLikeProps):
    def __init__(
        self,
        *,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
    ) -> None:
        '''
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a364b9ce1256fd29bb75cdb59f79a559f0150e404213d3d0a4547906d4273e)
            check_type(argname="argument group_ids", value=group_ids, expected_type=type_hints["group_ids"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
            check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
            check_type(argname="argument fill_style", value=fill_style, expected_type=type_hints["fill_style"])
            check_type(argname="argument opacity", value=opacity, expected_type=type_hints["opacity"])
            check_type(argname="argument roughness", value=roughness, expected_type=type_hints["roughness"])
            check_type(argname="argument roundness", value=roundness, expected_type=type_hints["roundness"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument stroke_style", value=stroke_style, expected_type=type_hints["stroke_style"])
            check_type(argname="argument stroke_width", value=stroke_width, expected_type=type_hints["stroke_width"])
            check_type(argname="argument end_arrowhead", value=end_arrowhead, expected_type=type_hints["end_arrowhead"])
            check_type(argname="argument end_binding", value=end_binding, expected_type=type_hints["end_binding"])
            check_type(argname="argument last_committed_point", value=last_committed_point, expected_type=type_hints["last_committed_point"])
            check_type(argname="argument start_arrowhead", value=start_arrowhead, expected_type=type_hints["start_arrowhead"])
            check_type(argname="argument start_binding", value=start_binding, expected_type=type_hints["start_binding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_ids is not None:
            self._values["group_ids"] = group_ids
        if height is not None:
            self._values["height"] = height
        if type is not None:
            self._values["type"] = type
        if width is not None:
            self._values["width"] = width
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y
        if background_color is not None:
            self._values["background_color"] = background_color
        if fill_style is not None:
            self._values["fill_style"] = fill_style
        if opacity is not None:
            self._values["opacity"] = opacity
        if roughness is not None:
            self._values["roughness"] = roughness
        if roundness is not None:
            self._values["roundness"] = roundness
        if stroke_color is not None:
            self._values["stroke_color"] = stroke_color
        if stroke_style is not None:
            self._values["stroke_style"] = stroke_style
        if stroke_width is not None:
            self._values["stroke_width"] = stroke_width
        if end_arrowhead is not None:
            self._values["end_arrowhead"] = end_arrowhead
        if end_binding is not None:
            self._values["end_binding"] = end_binding
        if last_committed_point is not None:
            self._values["last_committed_point"] = last_committed_point
        if start_arrowhead is not None:
            self._values["start_arrowhead"] = start_arrowhead
        if start_binding is not None:
            self._values["start_binding"] = start_binding

    @builtins.property
    def group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def background_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fill_style(self) -> typing.Optional[FillStyle]:
        result = self._values.get("fill_style")
        return typing.cast(typing.Optional[FillStyle], result)

    @builtins.property
    def opacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("opacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roughness(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("roughness")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roundness(self) -> typing.Any:
        result = self._values.get("roundness")
        return typing.cast(typing.Any, result)

    @builtins.property
    def stroke_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stroke_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stroke_style(self) -> typing.Optional[StrokeStyle]:
        result = self._values.get("stroke_style")
        return typing.cast(typing.Optional[StrokeStyle], result)

    @builtins.property
    def stroke_width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("stroke_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_arrowhead(self) -> typing.Any:
        result = self._values.get("end_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def end_binding(self) -> typing.Any:
        result = self._values.get("end_binding")
        return typing.cast(typing.Any, result)

    @builtins.property
    def last_committed_point(self) -> typing.Any:
        result = self._values.get("last_committed_point")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_arrowhead(self) -> typing.Any:
        result = self._values.get("start_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_binding(self) -> typing.Any:
        result = self._values.get("start_binding")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RectangleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Text(DrawnObject, metaclass=jsii.JSIIMeta, jsii_type="cdk-arch.Text"):
    def __init__(
        self,
        *,
        text: builtins.str,
        baseline: typing.Optional[jsii.Number] = None,
        container_id: typing.Any = None,
        font_family: typing.Optional[jsii.Number] = None,
        font_size: typing.Optional[jsii.Number] = None,
        line_height: typing.Optional[jsii.Number] = None,
        original_text: typing.Optional[builtins.str] = None,
        text_align: typing.Optional[builtins.str] = None,
        vertical_align: typing.Optional[builtins.str] = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param text: 
        :param baseline: 
        :param container_id: 
        :param font_family: 
        :param font_size: 
        :param line_height: 
        :param original_text: 
        :param text_align: 
        :param vertical_align: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        '''
        args = TextProps(
            text=text,
            baseline=baseline,
            container_id=container_id,
            font_family=font_family,
            font_size=font_size,
            line_height=line_height,
            original_text=original_text,
            text_align=text_align,
            vertical_align=vertical_align,
            background_color=background_color,
            fill_style=fill_style,
            opacity=opacity,
            roughness=roughness,
            roundness=roundness,
            stroke_color=stroke_color,
            stroke_style=stroke_style,
            stroke_width=stroke_width,
            group_ids=group_ids,
            height=height,
            type=type,
            width=width,
            x=x,
            y=y,
        )

        jsii.create(self.__class__, self, [args])

    @builtins.property
    @jsii.member(jsii_name="baseline")
    def baseline(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "baseline"))

    @baseline.setter
    def baseline(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f308c872b74ce6c5a0e83962aa3643de77b5d485a94f79edd2dc287b6c5047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseline", value)

    @builtins.property
    @jsii.member(jsii_name="containerId")
    def container_id(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "containerId"))

    @container_id.setter
    def container_id(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f8acd6e645a42b51f8d26772f23db4e7b446e7af89901b0156e20685201fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerId", value)

    @builtins.property
    @jsii.member(jsii_name="fontFamily")
    def font_family(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fontFamily"))

    @font_family.setter
    def font_family(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35bb3377381bf5e4fc7702bc10db9d611d5f35fa8a6ee5e3f42d47d201ff467c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fontFamily", value)

    @builtins.property
    @jsii.member(jsii_name="fontSize")
    def font_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fontSize"))

    @font_size.setter
    def font_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae848b42515fcaa51ede4340c30557c666eb6496881000154bf465742bd554ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fontSize", value)

    @builtins.property
    @jsii.member(jsii_name="lineHeight")
    def line_height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lineHeight"))

    @line_height.setter
    def line_height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be988d3842c5fc36a60b301e9ba65dcbf812ba0b71c0b6a7566ce7fb4aea290b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineHeight", value)

    @builtins.property
    @jsii.member(jsii_name="originalText")
    def original_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originalText"))

    @original_text.setter
    def original_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dafa851953708964cb6924f74267f0d21af303bb822d44540ec9acc6cb96537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originalText", value)

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cda2b76694f2317d02e1d20337f642cf1ac3c8a0b55f3cf5a1164f9bcf54ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value)

    @builtins.property
    @jsii.member(jsii_name="textAlign")
    def text_align(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textAlign"))

    @text_align.setter
    def text_align(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b7a23dbfb69fe002c23f19aecd0d417a5df4cb92a27c7e7f0410ea8bd006f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textAlign", value)

    @builtins.property
    @jsii.member(jsii_name="verticalAlign")
    def vertical_align(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verticalAlign"))

    @vertical_align.setter
    def vertical_align(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ac8601f3dc135f0cae2ffaa7e0fb7e230f3103638444ff8331580ff852c051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verticalAlign", value)


@jsii.data_type(
    jsii_type="cdk-arch.TextProps",
    jsii_struct_bases=[DrawnObjectProps],
    name_mapping={
        "group_ids": "groupIds",
        "height": "height",
        "type": "type",
        "width": "width",
        "x": "x",
        "y": "y",
        "background_color": "backgroundColor",
        "fill_style": "fillStyle",
        "opacity": "opacity",
        "roughness": "roughness",
        "roundness": "roundness",
        "stroke_color": "strokeColor",
        "stroke_style": "strokeStyle",
        "stroke_width": "strokeWidth",
        "text": "text",
        "baseline": "baseline",
        "container_id": "containerId",
        "font_family": "fontFamily",
        "font_size": "fontSize",
        "line_height": "lineHeight",
        "original_text": "originalText",
        "text_align": "textAlign",
        "vertical_align": "verticalAlign",
    },
)
class TextProps(DrawnObjectProps):
    def __init__(
        self,
        *,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        text: builtins.str,
        baseline: typing.Optional[jsii.Number] = None,
        container_id: typing.Any = None,
        font_family: typing.Optional[jsii.Number] = None,
        font_size: typing.Optional[jsii.Number] = None,
        line_height: typing.Optional[jsii.Number] = None,
        original_text: typing.Optional[builtins.str] = None,
        text_align: typing.Optional[builtins.str] = None,
        vertical_align: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param text: 
        :param baseline: 
        :param container_id: 
        :param font_family: 
        :param font_size: 
        :param line_height: 
        :param original_text: 
        :param text_align: 
        :param vertical_align: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4030316b43e306aa3154c66fa5e68f3204a296cc4e35688a760f3b63c602423b)
            check_type(argname="argument group_ids", value=group_ids, expected_type=type_hints["group_ids"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
            check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
            check_type(argname="argument fill_style", value=fill_style, expected_type=type_hints["fill_style"])
            check_type(argname="argument opacity", value=opacity, expected_type=type_hints["opacity"])
            check_type(argname="argument roughness", value=roughness, expected_type=type_hints["roughness"])
            check_type(argname="argument roundness", value=roundness, expected_type=type_hints["roundness"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument stroke_style", value=stroke_style, expected_type=type_hints["stroke_style"])
            check_type(argname="argument stroke_width", value=stroke_width, expected_type=type_hints["stroke_width"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            check_type(argname="argument baseline", value=baseline, expected_type=type_hints["baseline"])
            check_type(argname="argument container_id", value=container_id, expected_type=type_hints["container_id"])
            check_type(argname="argument font_family", value=font_family, expected_type=type_hints["font_family"])
            check_type(argname="argument font_size", value=font_size, expected_type=type_hints["font_size"])
            check_type(argname="argument line_height", value=line_height, expected_type=type_hints["line_height"])
            check_type(argname="argument original_text", value=original_text, expected_type=type_hints["original_text"])
            check_type(argname="argument text_align", value=text_align, expected_type=type_hints["text_align"])
            check_type(argname="argument vertical_align", value=vertical_align, expected_type=type_hints["vertical_align"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "text": text,
        }
        if group_ids is not None:
            self._values["group_ids"] = group_ids
        if height is not None:
            self._values["height"] = height
        if type is not None:
            self._values["type"] = type
        if width is not None:
            self._values["width"] = width
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y
        if background_color is not None:
            self._values["background_color"] = background_color
        if fill_style is not None:
            self._values["fill_style"] = fill_style
        if opacity is not None:
            self._values["opacity"] = opacity
        if roughness is not None:
            self._values["roughness"] = roughness
        if roundness is not None:
            self._values["roundness"] = roundness
        if stroke_color is not None:
            self._values["stroke_color"] = stroke_color
        if stroke_style is not None:
            self._values["stroke_style"] = stroke_style
        if stroke_width is not None:
            self._values["stroke_width"] = stroke_width
        if baseline is not None:
            self._values["baseline"] = baseline
        if container_id is not None:
            self._values["container_id"] = container_id
        if font_family is not None:
            self._values["font_family"] = font_family
        if font_size is not None:
            self._values["font_size"] = font_size
        if line_height is not None:
            self._values["line_height"] = line_height
        if original_text is not None:
            self._values["original_text"] = original_text
        if text_align is not None:
            self._values["text_align"] = text_align
        if vertical_align is not None:
            self._values["vertical_align"] = vertical_align

    @builtins.property
    def group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def background_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fill_style(self) -> typing.Optional[FillStyle]:
        result = self._values.get("fill_style")
        return typing.cast(typing.Optional[FillStyle], result)

    @builtins.property
    def opacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("opacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roughness(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("roughness")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roundness(self) -> typing.Any:
        result = self._values.get("roundness")
        return typing.cast(typing.Any, result)

    @builtins.property
    def stroke_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stroke_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stroke_style(self) -> typing.Optional[StrokeStyle]:
        result = self._values.get("stroke_style")
        return typing.cast(typing.Optional[StrokeStyle], result)

    @builtins.property
    def stroke_width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("stroke_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def text(self) -> builtins.str:
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def baseline(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("baseline")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def container_id(self) -> typing.Any:
        result = self._values.get("container_id")
        return typing.cast(typing.Any, result)

    @builtins.property
    def font_family(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("font_family")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def font_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("font_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_height(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("line_height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def original_text(self) -> typing.Optional[builtins.str]:
        result = self._values.get("original_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text_align(self) -> typing.Optional[builtins.str]:
        result = self._values.get("text_align")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vertical_align(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vertical_align")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TextProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-arch.ArrowProps",
    jsii_struct_bases=[LineProps],
    name_mapping={
        "group_ids": "groupIds",
        "height": "height",
        "type": "type",
        "width": "width",
        "x": "x",
        "y": "y",
        "background_color": "backgroundColor",
        "fill_style": "fillStyle",
        "opacity": "opacity",
        "roughness": "roughness",
        "roundness": "roundness",
        "stroke_color": "strokeColor",
        "stroke_style": "strokeStyle",
        "stroke_width": "strokeWidth",
        "end_arrowhead": "endArrowhead",
        "end_binding": "endBinding",
        "last_committed_point": "lastCommittedPoint",
        "start_arrowhead": "startArrowhead",
        "start_binding": "startBinding",
        "points": "points",
    },
)
class ArrowProps(LineProps):
    def __init__(
        self,
        *,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
        points: typing.Optional[typing.Sequence[typing.Sequence[jsii.Number]]] = None,
    ) -> None:
        '''
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        :param points: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620362c1454096dd80034fb5564abd3b04677bfc5d3fe510b3a0a295002e7363)
            check_type(argname="argument group_ids", value=group_ids, expected_type=type_hints["group_ids"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
            check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
            check_type(argname="argument fill_style", value=fill_style, expected_type=type_hints["fill_style"])
            check_type(argname="argument opacity", value=opacity, expected_type=type_hints["opacity"])
            check_type(argname="argument roughness", value=roughness, expected_type=type_hints["roughness"])
            check_type(argname="argument roundness", value=roundness, expected_type=type_hints["roundness"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument stroke_style", value=stroke_style, expected_type=type_hints["stroke_style"])
            check_type(argname="argument stroke_width", value=stroke_width, expected_type=type_hints["stroke_width"])
            check_type(argname="argument end_arrowhead", value=end_arrowhead, expected_type=type_hints["end_arrowhead"])
            check_type(argname="argument end_binding", value=end_binding, expected_type=type_hints["end_binding"])
            check_type(argname="argument last_committed_point", value=last_committed_point, expected_type=type_hints["last_committed_point"])
            check_type(argname="argument start_arrowhead", value=start_arrowhead, expected_type=type_hints["start_arrowhead"])
            check_type(argname="argument start_binding", value=start_binding, expected_type=type_hints["start_binding"])
            check_type(argname="argument points", value=points, expected_type=type_hints["points"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_ids is not None:
            self._values["group_ids"] = group_ids
        if height is not None:
            self._values["height"] = height
        if type is not None:
            self._values["type"] = type
        if width is not None:
            self._values["width"] = width
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y
        if background_color is not None:
            self._values["background_color"] = background_color
        if fill_style is not None:
            self._values["fill_style"] = fill_style
        if opacity is not None:
            self._values["opacity"] = opacity
        if roughness is not None:
            self._values["roughness"] = roughness
        if roundness is not None:
            self._values["roundness"] = roundness
        if stroke_color is not None:
            self._values["stroke_color"] = stroke_color
        if stroke_style is not None:
            self._values["stroke_style"] = stroke_style
        if stroke_width is not None:
            self._values["stroke_width"] = stroke_width
        if end_arrowhead is not None:
            self._values["end_arrowhead"] = end_arrowhead
        if end_binding is not None:
            self._values["end_binding"] = end_binding
        if last_committed_point is not None:
            self._values["last_committed_point"] = last_committed_point
        if start_arrowhead is not None:
            self._values["start_arrowhead"] = start_arrowhead
        if start_binding is not None:
            self._values["start_binding"] = start_binding
        if points is not None:
            self._values["points"] = points

    @builtins.property
    def group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def background_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fill_style(self) -> typing.Optional[FillStyle]:
        result = self._values.get("fill_style")
        return typing.cast(typing.Optional[FillStyle], result)

    @builtins.property
    def opacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("opacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roughness(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("roughness")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roundness(self) -> typing.Any:
        result = self._values.get("roundness")
        return typing.cast(typing.Any, result)

    @builtins.property
    def stroke_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stroke_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stroke_style(self) -> typing.Optional[StrokeStyle]:
        result = self._values.get("stroke_style")
        return typing.cast(typing.Optional[StrokeStyle], result)

    @builtins.property
    def stroke_width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("stroke_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_arrowhead(self) -> typing.Any:
        result = self._values.get("end_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def end_binding(self) -> typing.Any:
        result = self._values.get("end_binding")
        return typing.cast(typing.Any, result)

    @builtins.property
    def last_committed_point(self) -> typing.Any:
        result = self._values.get("last_committed_point")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_arrowhead(self) -> typing.Any:
        result = self._values.get("start_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_binding(self) -> typing.Any:
        result = self._values.get("start_binding")
        return typing.cast(typing.Any, result)

    @builtins.property
    def points(self) -> typing.Optional[typing.List[typing.List[jsii.Number]]]:
        result = self._values.get("points")
        return typing.cast(typing.Optional[typing.List[typing.List[jsii.Number]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArrowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-arch.EllipseProps",
    jsii_struct_bases=[LineLikeProps],
    name_mapping={
        "group_ids": "groupIds",
        "height": "height",
        "type": "type",
        "width": "width",
        "x": "x",
        "y": "y",
        "background_color": "backgroundColor",
        "fill_style": "fillStyle",
        "opacity": "opacity",
        "roughness": "roughness",
        "roundness": "roundness",
        "stroke_color": "strokeColor",
        "stroke_style": "strokeStyle",
        "stroke_width": "strokeWidth",
        "end_arrowhead": "endArrowhead",
        "end_binding": "endBinding",
        "last_committed_point": "lastCommittedPoint",
        "start_arrowhead": "startArrowhead",
        "start_binding": "startBinding",
    },
)
class EllipseProps(LineLikeProps):
    def __init__(
        self,
        *,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
    ) -> None:
        '''
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66aa7d49e1258aeaee1f1314de27dc1d583db69f3835b4330bffdce84b189d9)
            check_type(argname="argument group_ids", value=group_ids, expected_type=type_hints["group_ids"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
            check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
            check_type(argname="argument fill_style", value=fill_style, expected_type=type_hints["fill_style"])
            check_type(argname="argument opacity", value=opacity, expected_type=type_hints["opacity"])
            check_type(argname="argument roughness", value=roughness, expected_type=type_hints["roughness"])
            check_type(argname="argument roundness", value=roundness, expected_type=type_hints["roundness"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument stroke_style", value=stroke_style, expected_type=type_hints["stroke_style"])
            check_type(argname="argument stroke_width", value=stroke_width, expected_type=type_hints["stroke_width"])
            check_type(argname="argument end_arrowhead", value=end_arrowhead, expected_type=type_hints["end_arrowhead"])
            check_type(argname="argument end_binding", value=end_binding, expected_type=type_hints["end_binding"])
            check_type(argname="argument last_committed_point", value=last_committed_point, expected_type=type_hints["last_committed_point"])
            check_type(argname="argument start_arrowhead", value=start_arrowhead, expected_type=type_hints["start_arrowhead"])
            check_type(argname="argument start_binding", value=start_binding, expected_type=type_hints["start_binding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_ids is not None:
            self._values["group_ids"] = group_ids
        if height is not None:
            self._values["height"] = height
        if type is not None:
            self._values["type"] = type
        if width is not None:
            self._values["width"] = width
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y
        if background_color is not None:
            self._values["background_color"] = background_color
        if fill_style is not None:
            self._values["fill_style"] = fill_style
        if opacity is not None:
            self._values["opacity"] = opacity
        if roughness is not None:
            self._values["roughness"] = roughness
        if roundness is not None:
            self._values["roundness"] = roundness
        if stroke_color is not None:
            self._values["stroke_color"] = stroke_color
        if stroke_style is not None:
            self._values["stroke_style"] = stroke_style
        if stroke_width is not None:
            self._values["stroke_width"] = stroke_width
        if end_arrowhead is not None:
            self._values["end_arrowhead"] = end_arrowhead
        if end_binding is not None:
            self._values["end_binding"] = end_binding
        if last_committed_point is not None:
            self._values["last_committed_point"] = last_committed_point
        if start_arrowhead is not None:
            self._values["start_arrowhead"] = start_arrowhead
        if start_binding is not None:
            self._values["start_binding"] = start_binding

    @builtins.property
    def group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def background_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fill_style(self) -> typing.Optional[FillStyle]:
        result = self._values.get("fill_style")
        return typing.cast(typing.Optional[FillStyle], result)

    @builtins.property
    def opacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("opacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roughness(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("roughness")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def roundness(self) -> typing.Any:
        result = self._values.get("roundness")
        return typing.cast(typing.Any, result)

    @builtins.property
    def stroke_color(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stroke_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stroke_style(self) -> typing.Optional[StrokeStyle]:
        result = self._values.get("stroke_style")
        return typing.cast(typing.Optional[StrokeStyle], result)

    @builtins.property
    def stroke_width(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("stroke_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_arrowhead(self) -> typing.Any:
        result = self._values.get("end_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def end_binding(self) -> typing.Any:
        result = self._values.get("end_binding")
        return typing.cast(typing.Any, result)

    @builtins.property
    def last_committed_point(self) -> typing.Any:
        result = self._values.get("last_committed_point")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_arrowhead(self) -> typing.Any:
        result = self._values.get("start_arrowhead")
        return typing.cast(typing.Any, result)

    @builtins.property
    def start_binding(self) -> typing.Any:
        result = self._values.get("start_binding")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EllipseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Line(LineLike, metaclass=jsii.JSIIMeta, jsii_type="cdk-arch.Line"):
    def __init__(
        self,
        *,
        points: typing.Optional[typing.Sequence[typing.Sequence[jsii.Number]]] = None,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param points: 
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        '''
        args = LineProps(
            points=points,
            end_arrowhead=end_arrowhead,
            end_binding=end_binding,
            last_committed_point=last_committed_point,
            start_arrowhead=start_arrowhead,
            start_binding=start_binding,
            background_color=background_color,
            fill_style=fill_style,
            opacity=opacity,
            roughness=roughness,
            roundness=roundness,
            stroke_color=stroke_color,
            stroke_style=stroke_style,
            stroke_width=stroke_width,
            group_ids=group_ids,
            height=height,
            type=type,
            width=width,
            x=x,
            y=y,
        )

        jsii.create(self.__class__, self, [args])

    @builtins.property
    @jsii.member(jsii_name="points")
    def points(self) -> typing.List[typing.List[jsii.Number]]:
        return typing.cast(typing.List[typing.List[jsii.Number]], jsii.get(self, "points"))

    @points.setter
    def points(self, value: typing.List[typing.List[jsii.Number]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a9ef5c81c986a6924cb617eb60dfeb7acaf8404e1c4b8e93d6a796a3c085c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "points", value)


class Arrow(Line, metaclass=jsii.JSIIMeta, jsii_type="cdk-arch.Arrow"):
    def __init__(
        self,
        *,
        points: typing.Optional[typing.Sequence[typing.Sequence[jsii.Number]]] = None,
        end_arrowhead: typing.Any = None,
        end_binding: typing.Any = None,
        last_committed_point: typing.Any = None,
        start_arrowhead: typing.Any = None,
        start_binding: typing.Any = None,
        background_color: typing.Optional[builtins.str] = None,
        fill_style: typing.Optional[FillStyle] = None,
        opacity: typing.Optional[jsii.Number] = None,
        roughness: typing.Optional[jsii.Number] = None,
        roundness: typing.Any = None,
        stroke_color: typing.Optional[builtins.str] = None,
        stroke_style: typing.Optional[StrokeStyle] = None,
        stroke_width: typing.Optional[jsii.Number] = None,
        group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        height: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param points: 
        :param end_arrowhead: 
        :param end_binding: 
        :param last_committed_point: 
        :param start_arrowhead: 
        :param start_binding: 
        :param background_color: 
        :param fill_style: 
        :param opacity: 
        :param roughness: 
        :param roundness: 
        :param stroke_color: 
        :param stroke_style: 
        :param stroke_width: 
        :param group_ids: 
        :param height: 
        :param type: 
        :param width: 
        :param x: 
        :param y: 
        '''
        args = ArrowProps(
            points=points,
            end_arrowhead=end_arrowhead,
            end_binding=end_binding,
            last_committed_point=last_committed_point,
            start_arrowhead=start_arrowhead,
            start_binding=start_binding,
            background_color=background_color,
            fill_style=fill_style,
            opacity=opacity,
            roughness=roughness,
            roundness=roundness,
            stroke_color=stroke_color,
            stroke_style=stroke_style,
            stroke_width=stroke_width,
            group_ids=group_ids,
            height=height,
            type=type,
            width=width,
            x=x,
            y=y,
        )

        jsii.create(self.__class__, self, [args])


__all__ = [
    "AppState",
    "Arrow",
    "ArrowHead",
    "ArrowProps",
    "Binding",
    "BoundElement",
    "DrawnObject",
    "DrawnObjectProps",
    "Ellipse",
    "EllipseProps",
    "ExcaliDrawPrimitive",
    "ExcaliDrawPrimitiveProps",
    "FillStyle",
    "Icon",
    "Line",
    "LineLike",
    "LineLikeProps",
    "LineProps",
    "Rectangle",
    "RectangleProps",
    "Roundness",
    "SketchBuilder",
    "StrokeStyle",
    "Text",
    "TextAlign",
    "TextProps",
    "VerticalAlign",
]

publication.publish()

def _typecheckingstub__ab1b5a072db5320165d1c6b06de8faebc55825227b01c089757ce9afbc274fe5(
    *,
    grid_size: typing.Any,
    view_background_color: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54af41b23d2df745b9acbab7ed8c3f8cb5bd6fa1e2a61ff87e36487c8c88f6b(
    *,
    element_id: builtins.str,
    focus: jsii.Number,
    gap: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6754c85b8d47ae016d1e5f0ead6f596a886914e8af2cca7147db03050e016c3(
    *,
    id: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d7d7e2a37ff5a6a34fd6c14c450597ae7b490fee4ae49215abf41555107aff(
    element: ExcaliDrawPrimitive,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c189f02e5d5f92cbea9eb55ca318d8fd0b7c72ed5d7988dd483b4e0afb0adea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f111879e8cc5b64c8d18bd5c0922a702a517042d91b44860ff9e92b4430014e(
    value: typing.List[BoundElement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93f44f7a4f655147d77f804918dfee0f51bdc5f3d1d854ad000fe737c1c6ce5(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3fa03235d0cc13a57a6a81c164ade8dfd4b77415f149fa10c52112ef9e34dd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d2893fd63642dc63478281c5f8786e30a2f0b93327d659107235cfb0b889ce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db800d0773b1c17c437bb0338fa3f235e608ed0fe11a5581eff05673b742fd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83ab6be018dca84f96bbf5bae6d58630ddda66a0fa9e794bf57c141e5fd4bc3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1800345b4e65c2df95fe80e43e2405dc7834b4733b2ebfc348190434131ed5ce(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfba71bf31fcd278dec4d42e22d46f875824e04cd5266c7dbfbc17a1a6c95e9d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a86911b993700ce3b247fd41b3c205f66b7a6e1d4ec0541c8f0e338af048c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9597604abbde6d8bee00450844e06fb058c3aae95167ae363c740100f1d03596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cba1d3f51dfaa539695db9455a8d6d4afaa959ff5c697e43dd983a1796748a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6090be5c4eb7c96f523f85d31e5905f730d689074c6f3e051cfb88b90332fcc0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb25aacf45ba92f11e3bad14a82dfc8ea23c0a1bd6f2a0dd4140ba5918878ab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef06167fb2a721ff4b4b265c531c7c698660040727f40fa9e44b842bcbda454(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3040e9bc92098a365cefeade34ca2ac50892c720b22babb511e30aba46a113(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b22b9037f7475e7e948f10644eebd95f28d2c462b73f67b82e49d645ccc799(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee22f3a6f3f27673bcd2e04e25daf3880763678f6bb42c25e675badfcdd9c3bc(
    *,
    group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    height: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975f575bf69f5571570bd08f3b0c2ecde4dfc73d6a2f7e0b86d4f5396625825a(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1a57a529be3c82cfa1ab67d4ebaa2640eb0911bdbc6c0769b20775b471379a(
    icon_file: builtins.str,
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dea3c9521a816ab322412263464cd7323e491ccf3b862f977051de5d8a6f2a7(
    x: jsii.Number,
    y: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7055f4625f379e0de775bad1836cef96c83d45cd83706560856ac15d00e60f(
    value: Rectangle,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8397895529458deb3ef5a6499cc99a28ad44f4a511b7b56b70f6b6528f337d11(
    value: typing.List[ExcaliDrawPrimitive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc07c5e2cbc56a5a25da850c11d479f3712bcea4cef18ee6fc4ec431c10baadb(
    value: Text,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d8b8c44a6e92d896a292613905d455fe47b68e4d2b70c3ed95854f95a6bc15(
    *,
    type: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29830b4b892acf2e556bd163570ecc436a736c9f6dfe447324a2cc8f5fde87a(
    start_node_id: builtins.str,
    end_node_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbaeb8ddf94148aa74f0dbc0ad9296d0ab99803dd1fc0f6ca5f1e8b6f7c3eef7(
    node: _constructs_77d1e7e8.IConstruct,
    *,
    data: typing.Any,
    type: builtins.str,
    trace: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdba1e318804db715fa5633c8f5bccf7d78acda7a2952d58d1e4d4216eedc06(
    save_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb4fe00223b05d5aa286bca9debfa08e09ba6aeaa52344db48af0dabe146960(
    start_node_id: builtins.str,
    end_node_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a27775148d320656bb0b61d5dc8bb785f2ec5357bcf45e9c2bb28763a87e99(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30c62e2bba773276c31f578d188ef1b8e74d1789437adb3b9be9e59d45bcc79(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09d5766d1564ab796d7c6ce26dbcb5e83a09705db378ce48b0beef83e4fdca8(
    value: typing.List[Arrow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429cde3a253b2e03ed91c1925bc222937b12f27eee48f17f3dd955ad2837ffa8(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b139745652812d01e8d0a06fa0b2fd88fb461219e6b114be51a61f441a1d394c(
    value: typing.Mapping[builtins.str, Icon],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccd3bf03f8618e77520f79389281e9253317c4aeff026d46c273e80ad029112(
    *,
    group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    height: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
    background_color: typing.Optional[builtins.str] = None,
    fill_style: typing.Optional[FillStyle] = None,
    opacity: typing.Optional[jsii.Number] = None,
    roughness: typing.Optional[jsii.Number] = None,
    roundness: typing.Any = None,
    stroke_color: typing.Optional[builtins.str] = None,
    stroke_style: typing.Optional[StrokeStyle] = None,
    stroke_width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8440156e2fba197d0bf38a2beb21c0bbb07cb3c4352bbfd92e0de87dc6fb6a(
    *,
    group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    height: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
    background_color: typing.Optional[builtins.str] = None,
    fill_style: typing.Optional[FillStyle] = None,
    opacity: typing.Optional[jsii.Number] = None,
    roughness: typing.Optional[jsii.Number] = None,
    roundness: typing.Any = None,
    stroke_color: typing.Optional[builtins.str] = None,
    stroke_style: typing.Optional[StrokeStyle] = None,
    stroke_width: typing.Optional[jsii.Number] = None,
    end_arrowhead: typing.Any = None,
    end_binding: typing.Any = None,
    last_committed_point: typing.Any = None,
    start_arrowhead: typing.Any = None,
    start_binding: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d922aed9ee428fe5eab84a1b2311230bd05063663d106cbd9a62ae3a3b9b21(
    *,
    group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    height: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
    background_color: typing.Optional[builtins.str] = None,
    fill_style: typing.Optional[FillStyle] = None,
    opacity: typing.Optional[jsii.Number] = None,
    roughness: typing.Optional[jsii.Number] = None,
    roundness: typing.Any = None,
    stroke_color: typing.Optional[builtins.str] = None,
    stroke_style: typing.Optional[StrokeStyle] = None,
    stroke_width: typing.Optional[jsii.Number] = None,
    end_arrowhead: typing.Any = None,
    end_binding: typing.Any = None,
    last_committed_point: typing.Any = None,
    start_arrowhead: typing.Any = None,
    start_binding: typing.Any = None,
    points: typing.Optional[typing.Sequence[typing.Sequence[jsii.Number]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a364b9ce1256fd29bb75cdb59f79a559f0150e404213d3d0a4547906d4273e(
    *,
    group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    height: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
    background_color: typing.Optional[builtins.str] = None,
    fill_style: typing.Optional[FillStyle] = None,
    opacity: typing.Optional[jsii.Number] = None,
    roughness: typing.Optional[jsii.Number] = None,
    roundness: typing.Any = None,
    stroke_color: typing.Optional[builtins.str] = None,
    stroke_style: typing.Optional[StrokeStyle] = None,
    stroke_width: typing.Optional[jsii.Number] = None,
    end_arrowhead: typing.Any = None,
    end_binding: typing.Any = None,
    last_committed_point: typing.Any = None,
    start_arrowhead: typing.Any = None,
    start_binding: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f308c872b74ce6c5a0e83962aa3643de77b5d485a94f79edd2dc287b6c5047(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f8acd6e645a42b51f8d26772f23db4e7b446e7af89901b0156e20685201fe8(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bb3377381bf5e4fc7702bc10db9d611d5f35fa8a6ee5e3f42d47d201ff467c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae848b42515fcaa51ede4340c30557c666eb6496881000154bf465742bd554ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be988d3842c5fc36a60b301e9ba65dcbf812ba0b71c0b6a7566ce7fb4aea290b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dafa851953708964cb6924f74267f0d21af303bb822d44540ec9acc6cb96537(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cda2b76694f2317d02e1d20337f642cf1ac3c8a0b55f3cf5a1164f9bcf54ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b7a23dbfb69fe002c23f19aecd0d417a5df4cb92a27c7e7f0410ea8bd006f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ac8601f3dc135f0cae2ffaa7e0fb7e230f3103638444ff8331580ff852c051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4030316b43e306aa3154c66fa5e68f3204a296cc4e35688a760f3b63c602423b(
    *,
    group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    height: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
    background_color: typing.Optional[builtins.str] = None,
    fill_style: typing.Optional[FillStyle] = None,
    opacity: typing.Optional[jsii.Number] = None,
    roughness: typing.Optional[jsii.Number] = None,
    roundness: typing.Any = None,
    stroke_color: typing.Optional[builtins.str] = None,
    stroke_style: typing.Optional[StrokeStyle] = None,
    stroke_width: typing.Optional[jsii.Number] = None,
    text: builtins.str,
    baseline: typing.Optional[jsii.Number] = None,
    container_id: typing.Any = None,
    font_family: typing.Optional[jsii.Number] = None,
    font_size: typing.Optional[jsii.Number] = None,
    line_height: typing.Optional[jsii.Number] = None,
    original_text: typing.Optional[builtins.str] = None,
    text_align: typing.Optional[builtins.str] = None,
    vertical_align: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620362c1454096dd80034fb5564abd3b04677bfc5d3fe510b3a0a295002e7363(
    *,
    group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    height: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
    background_color: typing.Optional[builtins.str] = None,
    fill_style: typing.Optional[FillStyle] = None,
    opacity: typing.Optional[jsii.Number] = None,
    roughness: typing.Optional[jsii.Number] = None,
    roundness: typing.Any = None,
    stroke_color: typing.Optional[builtins.str] = None,
    stroke_style: typing.Optional[StrokeStyle] = None,
    stroke_width: typing.Optional[jsii.Number] = None,
    end_arrowhead: typing.Any = None,
    end_binding: typing.Any = None,
    last_committed_point: typing.Any = None,
    start_arrowhead: typing.Any = None,
    start_binding: typing.Any = None,
    points: typing.Optional[typing.Sequence[typing.Sequence[jsii.Number]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66aa7d49e1258aeaee1f1314de27dc1d583db69f3835b4330bffdce84b189d9(
    *,
    group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    height: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
    background_color: typing.Optional[builtins.str] = None,
    fill_style: typing.Optional[FillStyle] = None,
    opacity: typing.Optional[jsii.Number] = None,
    roughness: typing.Optional[jsii.Number] = None,
    roundness: typing.Any = None,
    stroke_color: typing.Optional[builtins.str] = None,
    stroke_style: typing.Optional[StrokeStyle] = None,
    stroke_width: typing.Optional[jsii.Number] = None,
    end_arrowhead: typing.Any = None,
    end_binding: typing.Any = None,
    last_committed_point: typing.Any = None,
    start_arrowhead: typing.Any = None,
    start_binding: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a9ef5c81c986a6924cb617eb60dfeb7acaf8404e1c4b8e93d6a796a3c085c4(
    value: typing.List[typing.List[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass
