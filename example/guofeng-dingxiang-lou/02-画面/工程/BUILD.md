# 本地代码制作

使用用户 `llm_new` Python 运行 `build.py`，复制既有音频并生成原生SVG、嘴形数据及HTML子合成；通过HyperFrames本地浏览器渲染。

无需图像/视频生成模型、API密钥或HeyGen登录。音频是已有AI翻唱素材，画面完全为代码绘制。剧照仅用于观察角色特征，没有拼贴照片进入画面。

`assets/鼎香楼.svg` 与 `assets/贾队长.svg` 是静态可编辑图形；HTML中嵌入相同图形供GSAP逐层动画。`build.py` 为生成源，重新运行会覆盖生成的HTML。
