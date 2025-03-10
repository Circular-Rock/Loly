<template>
  <div class="hello">
    <el-button type="primary">Primary Button</el-button>
    <el-button>Default Button</el-button>
    <el-button type="success">Success Button</el-button>
    <el-button type="info">Info Button</el-button>
    <el-button type="warning">Warning Button</el-button>
    <el-button type="danger">Danger Button</el-button>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>
