from datetime import datetime

class Task:
    def __init__(self,title,deadline,status):
        self.title = title
        self.deadline = deadline
        self.status = status

    def choose_color_day(self,cal):
        current_date = datetime.now().date()
        if current_date > self.deadline and self.status is False:
            cal.calevent_create(self.deadline,self.title, "code_red")
            cal.tag_config("code_red",background="red",foregraund="white")
        elif self.status is True:
            cal.calevent_create(self.deadline, self.title, "code_green")
            cal.tag_config("code_green", background="green", foreground="white")

        else:
            days = (self.deadline - current_date).days
            if  days <= 2:
                        cal.calevent_create(self.deadline, self.title, "code_orange")
                        cal.tag_config("code_orange", background="orange", foregraund="white")
            elif days <= 4:
                        cal.calevent_create(self.deadline, self.title, "code_yellow")
                        cal.tag_config("code_yellow", background="yellow", foregraund="white")
            elif days >= 5:
                        cal.calevent_create(self.deadline, self.title, "code_blue")
                        cal.tag_config("code_blue", background="blue", foregraund="white")





