<template>
  <div>
    <div class="waterfall">
      <viewer :images="items">
        <div
          class="item"
          v-for="(item,index) in items"
          :key="index"
        >
          <div class="item-content">
            <img
              v-lazy="item.img_url"
              alt=""
              srcset=""
            >
          </div>
        </div>
      </viewer>

    </div>
  </div>
</template>
<script>
import Viewer from "v-viewer";
import "viewerjs/dist/viewer.css";
import Vue from "vue";
import { getpic } from "../../api/test";
import VueLazyload from "vue-lazyload";
Vue.use(VueLazyload, {
  error: "https://upload-images.jianshu.io/upload_images/5546561-ac1125cddf6bcb67.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240", //图片加载失败时候显示的图片
  loading: "https://upload-images.jianshu.io/upload_images/5546561-c259c436d2395c79.jpg?imageMogr2/auto-orient/strip" //图片还未加载完成时候的loading图片
});
Vue.use(Viewer);
Viewer.setDefaults({
  Options: {
    inline: true,
    button: true,
    navbar: true,
    title: true,
    toolbar: true,
    tooltip: true,
    movable: true,
    zoomable: true,
    rotatable: true,
    scalable: true,
    transition: true,
    fullscreen: true,
    keyboard: true,
    url: "data-source"
  }
});
export default {
  data() {
    return {
      count: 20,
      page: 0,
      items: []
    };
  },
  computed: {},
  mounted: function() {},
  created() {
    let that = this;
    let data = {
      count: that.count,
      page: that.page
    };
    getpic(data).then(res => {
      console.log(res);
      that.items = res.data;
      that.page = that.page++;
    });
    window.onscroll = function() {
      if(that.page == 0){
        that.page = 1
      }
      //变量scrollTop是滚动条滚动时，距离顶部的距离
      var scrollTop =
        document.documentElement.scrollTop || document.body.scrollTop; //变量windowHeight是可视区的高度
      var windowHeight =
        document.documentElement.clientHeight || document.body.clientHeight; //变量scrollHeight是滚动条的总高度
      var scrollHeight =
        document.documentElement.scrollHeight || document.body.scrollHeight; //滚动条到底部的条件
      if (scrollTop + windowHeight == scrollHeight) {
        //写后台加载数据的函数
        let data = {
          count: that.count,
          page: that.page
        };
        getpic(data).then(res => {
          res.data.forEach(c => {
            that.items.push(c);
          });
          that.page = that.page + 1;
        });
      }
    };
  },

  methods: {},
  components: {
    // 组件
  }
};
</script>
<style>
@media (max-width:9000px) {
  .waterfall {
    width: 80%;
    margin: 0 auto;
    column-count: 6;
    column-gap: 0;
  }
}
@media (max-width:1300px) {
  .waterfall {
    width: 80%;
    margin: 0 auto;
    column-count: 6;
    column-gap: 0;
  }
}

@media (max-width:1080px) {
  .waterfall {
    width: 80%;
    margin: 0 auto;
    column-count: 6;
    column-gap: 0;
  }
}

@media (max-width:799px) {
  .waterfall {
    width: 80%;
    margin: 0 auto;
    column-count: 6;
    column-gap: 0;
  }
}

@media (max-width:720px) {
  .waterfall {
    width: 80%;
    margin: 0 auto;
    column-count: 6;
    column-gap: 0;
  }
}

@media (max-width:460px) {
  .waterfall {
    width: 94%;
    margin: 0 auto;
    column-count: 2;
    column-gap: 0;
  }
}

@media (max-height:750px) {
  .waterfall {
    width: 94%;
    margin: 0 auto;
    column-count: 2;
    column-gap: 0;
  }
}

@media (max-height:310px) {
  .waterfall {
    width: 94%;
    margin: 0 auto;
    column-count: 6;
    column-gap: 0;
  }
}

@media (max-height:260px) {
  .waterfall {
    width: 94%;
    margin: 0 auto;
    column-count: 6;
    column-gap: 0;
  }
}


.item {
  box-sizing: border-box;
  break-inside: avoid;
  padding: 10px;
}
.item-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 10px;
  height: auto;
  font-size: 20px;
  color: #686868;
  box-sizing: border-box;
}
img {
  width: 100%;
  border-radius: 10px;
}
</style>