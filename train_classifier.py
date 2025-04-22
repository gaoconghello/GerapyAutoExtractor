from gerapy_auto_extractor.classifiers.list import ListClassifier

if __name__ == '__main__':
    # 创建分类器实例
    classifier = ListClassifier()
    
    # 调用训练方法
    print("开始训练分类器...")
    classifier.train()
    print("训练完成！")
    
    # 可以打印模型路径，方便查看
    print(f"模型已保存到: {classifier.model_path}")
    print(f"特征缩放器已保存到: {classifier.scaler_path}")