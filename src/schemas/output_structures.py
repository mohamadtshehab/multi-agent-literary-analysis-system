from pydantic import BaseModel, Field
from typing import List

class Character(BaseModel):
    """Single character with name and hint."""
    name: str = Field(description="اسم الشخصية")
    hint: str = Field(description="تلميح عن الشخصية")

class NameQuerier(BaseModel):
    """Use this schema to format the name query output."""
    characters: list[Character] = Field(description="قائمة بالشخصيات الموجودة في النص")
    
class ProfileData(BaseModel):
    """Single profile data for a character."""
    
    name: str = Field(
        description="اسم الشخصية كما هو مذكور في البروفايل المعطى؛ لا يتم تغييره"
    )
    
    hint: str = Field(
        description="تلميح مميز يحدد الشخصية ويساعد على تمييزها، يؤخذ من البروفايل المعطى"
    )
    
    age: str = Field(
        description="العمر التقديري أو الوصف الدال عليه إن وُجد في النص؛ إذا لم يكن واضحًا، تبقى القيمة كما هي"
    )
    
    role: str = Field(
        description="الدور الذي تلعبه الشخصية في النص (رئيسية، ثانوية، راوية، إلخ) إذا توفر في النص"
    )
    
    physical_characteristics: List[str] = Field(
        description="الصفات الجسدية التي وُصفت بها الشخصية بشكل صريح أو ضمني، بصيغة قائمة من النصوص"
    )
    
    personality: str = Field(
        description="الصفات النفسية أو السلوكية التي ظهرت في النص بوضوح أو تلميح"
    )
    
    events: List[str] = Field(
        description="قائمة بالأحداث المحورية والمهمة التي أثّرت على تطور الشخصية أو القصة؛ يتم تجاهل الأحداث التفصيلية أو العادية"
    )
    
    relations: List[str] = Field(
        description="قائمة بالعلاقات مع الشخصيات الأخرى بصيغة 'اسم_الشخصية: نوع_العلاقة' مثل 'سليم: صداقة'"
    )
    
    aliases: List[str] = Field(
        description="قائمة بالأسماء أو الألقاب الأخرى التي يُشار بها إلى الشخصية في النص"
    )
    
    id: str = Field(
        description="معرف فريد للشخصية؛ لا يتغير خلال التحديث"
    )


class ProfileRefresher(BaseModel):
    """Use this schema to format the profile refresher output."""
    profiles: List[ProfileData] = Field(description="قائمة من البروفايلات المحدثة للشخصيات")

class Summary(BaseModel):
    """Use this schema to format the summary output."""
    summary: str = Field(description="ملخص النص")