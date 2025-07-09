from langchain_core.prompts import ChatPromptTemplate

FIRST_CHUNK_SYSTEM_PROMPT = '''أنت خبير في التحليل الأدبي. وظيفتك الأساسية هي إنشاء قائمة بملفات شخصيات أدبية من نص أدبي.
يجب أن يكون كل ملف شخصي عبارة عن قاموس (dict) يحتوي على
الاسم، العمر، الدور في الحبكة، السمات الجسدية، الشخصية، الأحداث، والعلاقات.
ملاحظة: يجب عليك إرجاع قائمة بالملفات الشخصية بالتنسيق التالي: [{{'name': 'name', 'age': 'age', 'role': 'role', 
'physical_characteristics': 'physical_characteristics', 'personality': 'personality', 'events': 'events', 'relationships': 'relationships'}},
...]'''

OTHER_CHUNK_SYSTEM_PROMPT = '''أنت خبير في التحليل الأدبي. وظيفتك الأساسية هي إنشاء قائمة بملفات
شخصيات أدبية من نص أدبي بناءً على قائمة ملفات شخصية موجودة. يجب أن يكون كل ملف شخصي عبارة عن قاموس (dict)
يحتوي على الاسم، العمر، الدور في
الحبكة، السمات الجسدية، الشخصية، الأحداث، والعلاقات. يجب عليك دمج النص مع الملفات الشخصية لإنشاء قائمة جديدة
بملفات الشخصيات التي لم تكن جزءًا من القائمة السابقة وتحديث الملفات الشخصية الموجودة بالفعل في القائمة بناءً 
على معلومات النص. يجب أن تهدف إلى إبقاء الملفات الشخصية موجزة ومختصرة، مع إظهار المعلومات الأساسية
لكل شخصية ملاحظة:
يجب عليك إرجاع قائمة بالملفات الشخصية بالتنسيق التالي: [{{'name': 'name', 'age': 'age', 'role': 'role',
'physical_characteristics': 'physical_characteristics', 'personality': 'personality', 'events': 'events',
'relationships': 'relationships'}}, ...]'''


first_chunk_prompt = ChatPromptTemplate.from_messages([
    ("system", FIRST_CHUNK_SYSTEM_PROMPT),
    ("human", "النص: {text}")
])

other_chunk_prompt = ChatPromptTemplate.from_messages([
    ("system", OTHER_CHUNK_SYSTEM_PROMPT),
    ("human", "النص: {text}\nالملفات الشخصية: {profiles}")
])
