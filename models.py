# -*- coding: utf-8 -*-
"""
Data models definition
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import json
import os


@dataclass
class Student:
    """Student data model"""
    name: str
    id: Optional[str] = None
    weight: float = 1.0  # Weight value for weighted selection
    picked_count: int = 0  # Times being picked
    last_picked: Optional[datetime] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'id': self.id,
            'weight': self.weight,
            'picked_count': self.picked_count,
            'last_picked': self.last_picked.isoformat() if self.last_picked else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create object from dictionary"""
        last_picked = None
        if data.get('last_picked'):
            last_picked = datetime.fromisoformat(data['last_picked'])
        return cls(
            name=data['name'],
            id=data.get('id'),
            weight=data.get('weight', 1.0),
            picked_count=data.get('picked_count', 0),
            last_picked=last_picked
        )


@dataclass
class PickRecord:
    """Pick record"""
    student_name: str
    timestamp: datetime
    rule_type: str
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'student_name': self.student_name,
            'timestamp': self.timestamp.isoformat(),
            'rule_type': self.rule_type
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create object from dictionary"""
        return cls(
            student_name=data['student_name'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            rule_type=data['rule_type']
        )


class DataManager:
    """Data manager"""
    
    def __init__(self, data_file: str = 'data.json'):
        self.data_file = data_file
        self.students: List[Student] = []
        self.records: List[PickRecord] = []
        self.load_data()
        # 如果数据文件不存在，创建空文件
        if not os.path.exists(self.data_file):
            self.save_data()
    
    def load_data(self):
        """Load data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.students = [Student.from_dict(s) for s in data.get('students', [])]
                    self.records = [PickRecord.from_dict(r) for r in data.get('records', [])]
            except Exception as e:
                print(f"Load data failed: {e}")
                self.students = []
                self.records = []
    
    def save_data(self):
        """Save data"""
        try:
            data = {
                'students': [s.to_dict() for s in self.students],
                'records': [r.to_dict() for r in self.records]
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Save data failed: {e}")
    
    def add_student(self, student: Student):
        """Add student"""
        self.students.append(student)
        self.save_data()
    
    def remove_student(self, name: str):
        """Remove student"""
        self.students = [s for s in self.students if s.name != name]
        self.save_data()
    
    def update_student(self, name: str, **kwargs):
        """Update student info"""
        for student in self.students:
            if student.name == name:
                for key, value in kwargs.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                self.save_data()
                return True
        return False
    
    def get_student(self, name: str) -> Optional[Student]:
        """Get student"""
        for student in self.students:
            if student.name == name:
                return student
        return None
    
    def add_record(self, record: PickRecord):
        """Add pick record"""
        self.records.append(record)
        self.save_data()
    
    def clear_all_students(self):
        """Clear all students"""
        self.students = []
        self.save_data()
    
    def reset_pick_counts(self):
        """Reset all pick counts"""
        for student in self.students:
            student.picked_count = 0
            student.last_picked = None
        self.save_data()
