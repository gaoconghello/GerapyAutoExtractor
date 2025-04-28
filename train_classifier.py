from gerapy_auto_extractor.classifiers.list import ListClassifier, is_list
from gerapy_auto_extractor.classifiers.detail import is_detail
import os
from glob import glob
import time
import argparse

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='训练和验证页面分类器')
    parser.add_argument('--train', action='store_true', help='是否进行训练')
    args = parser.parse_args()

    # 创建分类器实例
    classifier = ListClassifier()
    
    # 如果指定了--train参数，则进行训练
    if args.train:
        # 调用训练方法
        print("开始训练分类器...")
        classifier.train()
        print("训练完成！")
        
        # 可以打印模型路径，方便查看
        print(f"模型已保存到: {classifier.model_path}")
        print(f"特征缩放器已保存到: {classifier.scaler_path}")
    
    # 验证模型在测试集上的准确率
    print("\n开始验证模型准确率...")
    time.sleep(1)  # 稍微暂停，让前面的输出更清晰
    
    # 定义测试数据路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_list_dir = os.path.join(base_dir, 'datasets', 'test', 'list')
    test_detail_dir = os.path.join(base_dir, 'datasets', 'test', 'detail')
    
    # 验证列表页
    list_files = glob(os.path.join(test_list_dir, '*.html'))
    list_correct = 0
    print(f"\n测试列表页（共{len(list_files)}个文件）:")
    
    for file_path in list_files:
        file_name = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        result = is_list(html_content)
        status = "✓" if result else "✗"
        list_correct += 1 if result else 0
        print(f"{status} {file_name} - 预测为: {'列表页' if result else '详情页'}")
    
    # 验证详情页
    detail_files = glob(os.path.join(test_detail_dir, '*.html'))
    detail_correct = 0
    print(f"\n测试详情页（共{len(detail_files)}个文件）:")
    
    for file_path in detail_files:
        file_name = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        result = is_detail(html_content)
        status = "✓" if result else "✗"
        detail_correct += 1 if result else 0
        print(f"{status} {file_name} - 预测为: {'详情页' if result else '列表页'}")
    
    # 计算总体准确率
    total_files = len(list_files) + len(detail_files)
    total_correct = list_correct + detail_correct
    accuracy = (total_correct / total_files) * 100 if total_files > 0 else 0
    
    print("\n验证结果统计:")
    print(f"列表页准确率: {list_correct}/{len(list_files)} ({list_correct/len(list_files)*100:.2f}%)" if len(list_files) > 0 else "列表页准确率: 无测试文件")
    print(f"详情页准确率: {detail_correct}/{len(detail_files)} ({detail_correct/len(detail_files)*100:.2f}%)" if len(detail_files) > 0 else "详情页准确率: 无测试文件")
    print(f"总体准确率: {total_correct}/{total_files} ({accuracy:.2f}%)" if total_files > 0 else "总体准确率: 无测试文件")