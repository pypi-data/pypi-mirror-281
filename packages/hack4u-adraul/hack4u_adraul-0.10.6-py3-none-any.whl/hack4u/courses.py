class Course:
    def __init__(self,name,duration,link):
        self.name = name
        self.duration = duration
        self.link = link
    
    def __repr__(self) -> str:
        return f"course name: {self.name}\nduration: {self.duration}\nlink: {self.link}"

courses =[
    Course("Introduccion a Linux",15,"link1"),
    Course("Personalizacion de Linux",3,"link2"),
    Course("Introduccion al Hacking",53,"link3"),
]

def list_courses():
    for c in courses:
        print(c)

def search_by_name(name):
    for c in courses:
        if c.name == name:
            return c
    return None

def print_numnber(n):
    print(n)