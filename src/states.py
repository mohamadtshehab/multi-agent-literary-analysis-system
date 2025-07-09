from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from src.data_classes import Profile


class State(TypedDict):
    profiles: Annotated[list[Profile], add_messages]
    chunks: Annotated[list[str], add_messages]
    porcessed_chunks: Annotated[list[str], add_messages]


initial_state = {
    'chunks': [''' في قديم الزمان، في أرض بعيدة جدًا، كانت هناك فتاة شابة تدعى أليس. كانت معروفة بفضولها وحبها للمغامرة. في أحد الأيام، قررت الشروع في رحلة للعثور على بلورة الحكمة الأسطورية.''',
                '''كانت الرحلة طويلة ومليئة بالتحديات، فقد كان على أليس عبور غابة خطيرة، والإبحار في نهر غادر، وتسلق جبل شاهق. على طول الطريق، التقت برجل عجوز حكيم أعطاها خريطة وبوصلة. بفضل الخريطة والبوصلة، تمكنت أليس من العثور على طريقها والوصول إلى وجهتها.'''],
    'profiles': [],
    'porcessed_chunks': []
}
