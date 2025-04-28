import asyncio
import logging
import re
import os
from urllib.parse import urlparse
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fetch_and_save_html(url: str, url_type: str = "list", base_dir: str = "datasets"):
    """
    获取URL的原始HTML内容并保存到文件
    
    参数:
      url: 要抓取的URL
      url_type: URL类型，可以是"list"或"detail"
      base_dir: 保存文件的基础目录
    """
    try:
        # 直接使用playwright获取HTML
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            # 阻止图片请求以加快速度
            await page.route("**/*.{png,jpg,jpeg,gif,webp}", lambda route: route.abort())
            
            try:
                logger.info(f"正在访问 {url}")
                # 等待页面加载完成
                await page.goto(url, timeout=60000, wait_until="domcontentloaded")
                # 等待一段时间让JavaScript执行
                await page.wait_for_timeout(5000)
                # 获取完整HTML
                html_content = await page.content()
                
                # 提取域名，去掉www前缀
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                domain = re.sub(r'^www\.', '', domain)
                
                # 如果域名包含端口号，去掉端口号
                domain = domain.split(':')[0]
                
                # 将域名中的点替换为下划线
                domain = domain.replace('.', '_')
                
                # 构建文件名
                filename_base = domain
                
                # 对detail类型URL，提取最后一个/后的内容作为文件名的一部分
                if url_type == "detail":
                    path = parsed_url.path
                    # 获取路径中最后一个/后的内容
                    last_segment = path.split('/')[-1]
                    # 如果最后一个部分为空（URL以/结尾），则使用倒数第二个部分
                    if not last_segment and len(path.split('/')) > 2:
                        last_segment = path.split('/')[-2]
                    # 如果还是没有提取到有效部分，使用整个路径的哈希值
                    if not last_segment:
                        last_segment = f"path_{hash(path) % 10000}"
                    # 替换特殊字符
                    last_segment = re.sub(r'[^\w]', '_', last_segment)
                    # 将.替换为_
                    last_segment = last_segment.replace('.', '_')
                    # 组合文件名
                    filename_base = f"{domain}_{last_segment}"
                
                # 确保datasets目录和子目录存在
                datasets_dir = os.path.join(base_dir, url_type)
                if not os.path.exists(datasets_dir):
                    os.makedirs(datasets_dir)
                    logger.info(f"创建目录: {datasets_dir}")
                
                # 构建文件路径
                filename = os.path.join(datasets_dir, f"{filename_base}.html")
                
                # 保存HTML到文件
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info(f"HTML已保存到文件: {filename}")
                
            except Exception as e:
                logger.error(f"获取页面内容失败: {e}")
            finally:
                await browser.close()
    except Exception as e:
        logger.error(f"playwright运行错误: {e}")

async def read_urls_and_fetch(filename: str, url_type: str, base_dir: str = "datasets"):
    """
    从文件中读取URL列表并获取HTML
    
    参数:
      filename: 包含URL列表的文件名
      url_type: URL类型，可以是"list"或"detail"
      base_dir: 保存文件的基础目录
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        logger.info(f"从{filename}文件中读取到{len(urls)}个URL")
        
        # 并发执行，每次最多10个任务
        batch_size = 10
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            tasks = [fetch_and_save_html(url, url_type, base_dir) for url in batch]
            await asyncio.gather(*tasks)
            
    except Exception as e:
        logger.error(f"读取URL文件失败: {e}")

async def main():
    # 命令行参数处理
    import sys
    
    # 检查是否包含 --test 参数
    is_test = "--test" in sys.argv
    
    # 根据是否测试模式调整保存路径
    save_dir = "datasets/test" if is_test else "datasets"
    
    if len(sys.argv) > 1 and not is_test:
        url = sys.argv[1]
        await fetch_and_save_html(url, "detail", save_dir)
    else:
        # 处理list.txt和detail.txt文件
        logger.info("开始处理list.txt和detail.txt文件")
        logger.info(f"保存目录: {save_dir}")
        
        # 处理列表页
        list_path = os.path.join("datasets", "list.txt")
        if os.path.exists(list_path):
            await read_urls_and_fetch(list_path, "list", save_dir)
        else:
            logger.warning(f"{list_path}文件不存在")
        
        # 处理详情页
        detail_path = os.path.join("datasets", "detail.txt")
        if os.path.exists(detail_path):
            await read_urls_and_fetch(detail_path, "detail", save_dir)
        else:
            logger.warning(f"{detail_path}文件不存在")

if __name__ == "__main__":
    asyncio.run(main())
