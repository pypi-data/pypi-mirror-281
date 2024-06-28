=============
WebviewRevise
=============

WebviewRevise 是一个基于 PyWebView 5.1 版本的修改版本，集成了网络拦截功能(该功能目前仅支持 EdgeChromium 作为后端引擎)。

概述
----

PyWebView 是一个轻量级的跨平台库，用于在 Python 应用程序中创建和控制 Webview 窗口。本项目在原有的基础上进行了扩展，添加了网络拦截功能，允许开发者拦截和修改通过 Webview 发送的网络请求。

特性
----

- 基于 PyWebView 5.1。
- 网络拦截功能，允许开发者：
    - 拦截 HTTP 请求和响应。
    - 修改请求头和响应头。
- 允许开发者自己控制CoreWebView2。
    - 只需要继承filter,在 do 方法中设置即可

安装
----

使用 pip 安装 WebviewRevise ：

.. code-block:: bash

    pip install WebviewRevise

请注意，由于本项目是 PyWebView 的修改版本，可能需要从源代码安装或使用特定的安装步骤。

使用示例
--------

以下是一个简单的使用示例，展示如何创建一个带有网络拦截功能的 Webview 窗口：

.. code-block:: python

    import webview
    from webview.platforms.edgechromium import DoSomething,filter,WebView2Core
    from webview.platforms.winforms import BrowserMap

    class net(filter):
        def do(self, edgeChrome, sender, args):
            # 开启请求过滤
            sender.CoreWebView2.AddWebResourceRequestedFilter("*", WebView2Core.CoreWebView2WebResourceContext.All) # *:表示所有
            # 网络请求拦截回调设置
            sender.CoreWebView2.WebResourceRequested += self.on_web_resource_requested # 设置回调函数

        def on_web_resource_requested(self, sender, args):
            """网络请求拦截回调函数:
                如果需要修改请求或响应，可以在这里进行操作

            Args:
                sender (_type_): Microsoft.Web.WebView2.Core.CoreWebView2 对象
                args (_type_): Microsoft.Web.WebView2.Core.CoreWebView2WebResourceRequestedEventArgs对象
            """        
            # 例如，打印请求的 URI
            print(args.Request.Uri)
            # 详情请参照 Microsoft.Web.WebView2 如何使用

   
    if __name__ == '__main__':
        # 创建 Webview 窗口并设置网络请求拦截器
        DoSomething.append(net())
        window = webview.create_window('Simple browser',"src/index.html")
        window.events.loaded += on_loaded
        window.is_filter = True # 默认开启过滤拦截
        webview.start(init,window)

贡献
----

我们欢迎任何形式的贡献，包括但不限于：

- 报告问题或错误。
- 提供功能请求或改进建议。

许可证
------

本项目采用 Modified BSD 许可证。有关更多信息，请查看 `LICENSE` 文件。
