import json
import time
from datetime import datetime
from typing import Dict, Any

# 模拟大模型API调用（实际项目中替换为真实API）
class MockLLMClient:
    """模拟大模型客户端，用于生成摘要"""
    
    def generate_summary(self, note_content: str, max_length: int = 100) -> str:
        """
        模拟大模型生成摘要
        
        参数:
            note_content: 笔记内容
            max_length: 摘要最大长度
            
        返回:
            生成的摘要文本
        """
        # 模拟API调用延迟
        time.sleep(0.5)
        
        # 简单的摘要逻辑（实际项目中使用真实的大模型API）
        sentences = note_content.split('。')
        if len(sentences) > 1:
            summary = sentences[0] + "。"
        else:
            summary = note_content[:max_length]
            
        # 确保摘要不超过指定长度
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
            
        return summary

class NoteAssistant:
    """AI智能笔记助手核心类"""
    
    def __init__(self):
        """初始化笔记助手"""
        self.llm_client = MockLLMClient()
        self.notes = []
        self.stats = {
            "total_notes": 0,
            "total_summaries": 0,
            "last_updated": None
        }
    
    def add_note(self, title: str, content: str, tags: list = None) -> Dict[str, Any]:
        """
        添加新笔记并自动生成摘要
        
        参数:
            title: 笔记标题
            content: 笔记内容
            tags: 标签列表
            
        返回:
            包含摘要的笔记对象
        """
        # 生成摘要
        summary = self.llm_client.generate_summary(content)
        
        # 创建笔记对象
        note = {
            "id": len(self.notes) + 1,
            "title": title,
            "content": content,
            "summary": summary,
            "tags": tags or [],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 保存笔记
        self.notes.append(note)
        
        # 更新统计信息
        self.stats["total_notes"] += 1
        self.stats["total_summaries"] += 1
        self.stats["last_updated"] = note["created_at"]
        
        return note
    
    def get_sidebar_summary(self, note_id: int = None) -> Dict[str, Any]:
        """
        获取侧边栏摘要显示（模拟悬浮交互流程）
        
        参数:
            note_id: 笔记ID，为None时返回最新笔记
            
        返回:
            侧边栏摘要数据
        """
        if not self.notes:
            return {"error": "暂无笔记"}
        
        if note_id is None:
            # 默认显示最新笔记
            note = self.notes[-1]
        else:
            # 查找指定ID的笔记
            note = next((n for n in self.notes if n["id"] == note_id), None)
            if not note:
                return {"error": "笔记不存在"}
        
        # 侧边栏摘要格式（模拟优化后的交互设计）
        sidebar_data = {
            "note_id": note["id"],
            "title": note["title"],
            "summary": note["summary"],
            "tags": note["tags"],
            "preview_length": len(note["summary"]),
            "display_time": datetime.now().strftime("%H:%M:%S"),
            "interaction_type": "sidebar_floating"
        }
        
        return sidebar_data
    
    def export_notes(self, format_type: str = "json") -> str:
        """
        导出笔记数据
        
        参数:
            format_type: 导出格式
            
        返回:
            导出的数据字符串
        """
        data = {
            "notes": self.notes,
            "statistics": self.stats,
            "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if format_type == "json":
            return json.dumps(data, ensure_ascii=False, indent=2)
        else:
            # 简单文本格式
            text_lines = []
            text_lines.append("=== AI智能笔记助手导出 ===")
            text_lines.append(f"导出时间: {data['exported_at']}")
            text_lines.append(f"笔记总数: {self.stats['total_notes']}")
            text_lines.append(f"摘要总数: {self.stats['total_summaries']}")
            text_lines.append("\n--- 笔记列表 ---")
            
            for note in self.notes:
                text_lines.append(f"\n[{note['id']}] {note['title']}")
                text_lines.append(f"摘要: {note['summary']}")
                text_lines.append(f"标签: {', '.join(note['tags'])}")
                text_lines.append(f"创建时间: {note['created_at']}")
            
            return "\n".join(text_lines)

def main():
    """主函数 - 演示AI智能笔记助手核心功能"""
    print("🚀 AI智能笔记助手启动中...\n")
    
    # 初始化助手
    assistant = NoteAssistant()
    
    # 演示添加笔记并生成摘要
    print("1. 添加笔记并自动生成摘要：")
    sample_notes = [
        {
            "title": "项目会议记录",
            "content": "今天讨论了AI产品的新交互设计。团队决定采用侧边栏悬浮式摘要功能，这将提升用户的信息提炼效率。下一步是进行A/B测试验证效果。",
            "tags": ["会议", "产品设计", "AI"]
        },
        {
            "title": "学习笔记 - 大模型应用",
            "content": "大模型在文本摘要任务中表现出色。通过适当的提示工程和交互设计，可以显著提升用户体验。关键指标包括任务完成率和用户停留时长。",
            "tags": ["学习", "AI", "技术"]
        }
    ]
    
    for note_data in sample_notes:
        note = assistant.add_note(
            title=note_data["title"],
            content=note_data["content"],
            tags=note_data["tags"]
        )
        print(f"   📝 已添加: {note['title']}")
        print(f"     摘要: {note['summary']}")
    
    print(f"\n2. 侧边栏悬浮摘要展示（模拟优化后的交互流程）：")
    sidebar_data = assistant.get_sidebar_summary()
    print(f"   🎯 当前聚焦笔记: {sidebar_data['title']}")
    print(f"   📋 智能摘要: {sidebar_data['summary']}")
    print(f"   🏷️  标签: {', '.join(sidebar_data['tags'])}")
    print(f"   ⏰ 显示时间: {sidebar_data['display_time']}")
    
    print(f"\n3. 统计信息：")
    print(f"   总笔记数: {assistant.stats['total_notes']}")
    print(f"   总摘要数: {assistant.stats['total_summaries']}")
    print(f"   最后更新: {assistant.stats['last_updated']}")
    
    print(f"\n4. 导出数据演示（JSON格式前100字符）：")
    exported = assistant.export_notes("json")
    print(f"   {exported[:100]}...")
    
    print(f"\n✅ 演示完成！")
    print("💡 提示：在实际项目中，MockLLMClient应替换为真实的大模型API调用")

if __name__ == "__main__":
    main()