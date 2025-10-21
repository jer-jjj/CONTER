# -*- coding: utf-8 -*-
"""
Business logic services
"""
import random
from typing import List, Optional
from datetime import datetime
import asyncio
from models import Student, PickRecord, DataManager
import openpyxl
import pandas as pd


class PickerService:
    """Picker service"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    async def pick_random(self, count: int = 1, exclude_picked: bool = False) -> List[Student]:
        """
        Random pick
        :param count: Number of students to pick
        :param exclude_picked: Whether to exclude picked students
        """
        await asyncio.sleep(0.01)  # Simulate async operation
        
        candidates = self.data_manager.students.copy()
        
        if exclude_picked:
            candidates = [s for s in candidates if s.picked_count == 0]
        
        if not candidates:
            return []
        
        count = min(count, len(candidates))
        picked = random.sample(candidates, count)
        
        # Update picked info
        for student in picked:
            original = self.data_manager.get_student(student.name)
            if original:
                original.picked_count += 1
                original.last_picked = datetime.now()
                # Record pick history
                record = PickRecord(
                    student_name=student.name,
                    timestamp=datetime.now(),
                    rule_type='Random Pick'
                )
                self.data_manager.add_record(record)
        
        self.data_manager.save_data()
        return picked
    
    async def pick_weighted(self, count: int = 1) -> List[Student]:
        """
        Weighted pick - Higher weight, higher probability
        :param count: Number of students to pick
        """
        await asyncio.sleep(0.01)
        
        candidates = self.data_manager.students.copy()
        if not candidates:
            return []
        
        # 无放回加权抽取（避免重复）
        count = min(count, len(candidates))
        working_pool = candidates.copy()
        picked: List[Student] = []
        
        while len(picked) < count and working_pool:
            weights = [max(0.000001, s.weight) for s in working_pool]
            chosen = random.choices(working_pool, weights=weights, k=1)[0]
            picked.append(chosen)
            # 从候选池移除，确保无放回
            working_pool = [s for s in working_pool if s.name != chosen.name]
        
        # Update picked info
        for student in picked:
            original = self.data_manager.get_student(student.name)
            if original:
                original.picked_count += 1
                original.last_picked = datetime.now()
                record = PickRecord(
                    student_name=student.name,
                    timestamp=datetime.now(),
                    rule_type='Weighted Pick'
                )
                self.data_manager.add_record(record)
        
        self.data_manager.save_data()
        return picked
    
    async def pick_least_picked(self, count: int = 1) -> List[Student]:
        """
        Pick students with least pick count
        :param count: Number of students to pick
        """
        await asyncio.sleep(0.01)
        
        candidates = self.data_manager.students.copy()
        if not candidates:
            return []
        
        # 按被抽取次数升序分组，逐层填充直至满足人数
        candidates.sort(key=lambda s: (s.picked_count, s.name))
        picked: List[Student] = []
        remaining = min(count, len(candidates))
        
        i = 0
        n = len(candidates)
        while remaining > 0 and i < n:
            current_count = candidates[i].picked_count
            group = []
            while i < n and candidates[i].picked_count == current_count:
                group.append(candidates[i])
                i += 1
            take = min(remaining, len(group))
            picked.extend(random.sample(group, take))
            remaining -= take
        
        # Update picked info
        for student in picked:
            original = self.data_manager.get_student(student.name)
            if original:
                original.picked_count += 1
                original.last_picked = datetime.now()
                record = PickRecord(
                    student_name=student.name,
                    timestamp=datetime.now(),
                    rule_type='Least Pick'
                )
                self.data_manager.add_record(record)
        
        self.data_manager.save_data()
        return picked
    
    async def animate_pick(self, duration: float = 2.0, final_result: List[Student] = None) -> List[str]:
        """
        Simulate pick animation, return random name sequence
        :param duration: Animation duration in seconds
        :param final_result: Final result
        """
        animation_names = []
        candidates = self.data_manager.students
        
        if not candidates:
            return []
        
        # Generate animation frames
        frames = int(duration * 10)  # 10 frames per second
        for i in range(frames):
            random_student = random.choice(candidates)
            animation_names.append(random_student.name)
            await asyncio.sleep(0.1)
        
        return animation_names


class ExcelService:
    """Excel import service"""
    
    @staticmethod
    async def import_from_excel(file_path: str) -> List[Student]:
        """
        Import student list from Excel file
        Supported format:
        - First column: Name (required)
        - Second column: Student ID (optional)
        - Third column: Weight (optional, default 1.0)
        """
        students = []
        
        try:
            # Use pandas to read Excel
            df = pd.read_excel(file_path)
            
            for index, row in df.iterrows():
                # Get name (required)
                name = str(row.iloc[0]).strip()
                if not name or name == 'nan':
                    continue
                
                # Get student ID (optional)
                student_id = None
                if len(row) > 1:
                    student_id = str(row.iloc[1]).strip()
                    if student_id == 'nan':
                        student_id = None
                
                # Get weight (optional)
                weight = 1.0
                if len(row) > 2:
                    try:
                        weight = float(row.iloc[2])
                        if weight <= 0:
                            weight = 1.0
                    except:
                        weight = 1.0
                
                student = Student(
                    name=name,
                    id=student_id,
                    weight=weight
                )
                students.append(student)
            
            await asyncio.sleep(0.01)  # Simulate async operation
            return students
            
        except Exception as e:
            raise Exception(f"Import Excel failed: {str(e)}")
    
    @staticmethod
    async def export_to_excel(students: List[Student], file_path: str):
        """
        Export student list to Excel
        """
        try:
            data = {
                'Name': [s.name for s in students],
                'ID': [s.id if s.id else '' for s in students],
                'Weight': [s.weight for s in students],
                'Pick Count': [s.picked_count for s in students],
                'Last Picked': [s.last_picked.strftime('%Y-%m-%d %H:%M:%S') if s.last_picked else '' for s in students]
            }
            
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            
            await asyncio.sleep(0.01)
            
        except Exception as e:
            raise Exception(f"Export Excel failed: {str(e)}")


class StatisticsService:
    """Statistics service"""
    
    @staticmethod
    def get_statistics(data_manager: DataManager) -> dict:
        """Get statistics info"""
        total_students = len(data_manager.students)
        total_picks = sum(s.picked_count for s in data_manager.students)
        
        picked_students = [s for s in data_manager.students if s.picked_count > 0]
        unpicked_students = [s for s in data_manager.students if s.picked_count == 0]
        
        most_picked = None
        if picked_students:
            most_picked = max(picked_students, key=lambda s: s.picked_count)
        
        return {
            'total_students': total_students,
            'total_picks': total_picks,
            'picked_count': len(picked_students),
            'unpicked_count': len(unpicked_students),
            'most_picked': most_picked,
            'recent_records': data_manager.records[-10:] if data_manager.records else []
        }
