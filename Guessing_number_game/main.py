from tkinter import*
import tkinter.messagebox as tmsg
import random
import pygame


class Geometry(Tk):
    '''Setting up the geometry of the game window  '''
    def __init__(self):
        super().__init__()
        screen_width = 800
        screen_height = 500
        x = (self.winfo_screenwidth() - screen_width)//2
        y = (self.winfo_screenheight()-screen_height)//2
        self.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
        self.resizable(False,False)
        self.title('Guess')
        self.config(background="#87CEFA")




class Sound:
    '''Class for handling game sounds'''
    pygame.mixer.init()
    def correct_answer_sound(self):
        '''Play sound for correct answer'''
        try:
            sound = pygame.mixer.Sound('win_sound.wav')
            sound.play()
    
        except FileNotFoundError:
            tmsg.showerror("Error",''''"win_sound.wav" not found ''')
    
        except Exception:
            tmsg.showerror("Error","An unknown error has occured")



    def wrong_answer_sound(self):
        '''Play sound for wrong answer'''
        try:
            sound = pygame.mixer.Sound('wrong_answer_sound.wav')
            sound.play()
    
        except FileNotFoundError:
            tmsg.showerror("Error",''''"wrong_answer_sound.wav" not found ''')
    
        except Exception:
            tmsg.showerror("Error","An unknown error has occured")



    def attempts_failed_sound(self):
        '''Play sound for all attempts failed'''
        try:
            sound = pygame.mixer.Sound('attempts_failed_sound.wav')
            sound.play()
    
        except FileNotFoundError:
            tmsg.showerror("Error",''''"attempts_failed_sound.wav" not found ''')

        except Exception:
            tmsg.showerror("Error","An unknown error has occured")



    def click_sound(self,event):
        '''Play sound if user clicks any other buttons'''
        try:
            sound = pygame.mixer.Sound('click_sound.wav')
            sound.play()

        except FileNotFoundError:
            tmsg.showerror("Error",''''"click_sound.wav" not found ''')

        except Exception as e:
            tmsg.showerror("Error","An unknown error has occured")




class Message_Display(Geometry):
    '''Class for displaying game messages.'''
    def correct_answer_message(self):
        '''display correct answer message when user guess the correct number'''
        for window in self.winfo_children():
            window.destroy()
        
        you_won = Label(text="Correct Guess!",font='verdana 22 bold',background="#87CEFA",foreground="#3B3B3B")
        you_won.pack(anchor='center',expand=True)
        self.after(1000,self.display_options)



    def all_attempts_failed(self):
        '''display all attempts failed message when user use all attempts and fails to guess new number also display the what was the correct answer'''
        for window in self.winfo_children():
            window.destroy()
        # Display the Attempts failed message and correct answer 
        frame = Frame(background="#87CEFA")
        Attempts_failed = Label(frame,text="All attempts failed",font='verdana 21 normal',background="#87CEFA")
        correct_answer = Label(frame,text=f"Correct answer was {self.answer}",font="verdana 15 normal",background="#3B3B3B",foreground="white",width=17,pady=4,padx=4)
        Attempts_failed.pack(ipadx=10)
        correct_answer.pack(pady=10,ipadx=10)
        
        # Play again button if user wants to play again
        play_again_button = Button(frame,text="Play Again",command=self.display_options,width=10,font='verdana 12 normal')
        play_again_button.bind("<Button-1>",self.click_sound)
        play_again_button.pack(ipadx=2,pady=10)
        frame.pack(anchor='center',expand=True)

        # Main menu button 
        main_menu = Button(text="Main Menu",font='verdana 12 normal',command=self.loading_mainMenu,foreground="white",background="#191970")
        main_menu.bind("<Button-1>",self.click_sound)
        main_menu.pack(anchor='ne',padx=15,pady=10,ipadx=5,ipady=5)



    def wrong_guess_message(self):
        ''' display short message "Wrong guess" for half seconds  when user guuess wrong answer'''            
        self.wrong_Answer = Label(text="Wrong guess",font="helvetica 15 bold",width=14,height=1,foreground="#FF3030",pady=3,background="#87CEFA")
        self.wrong_Answer.place(x=317,y=100)
        # after half seconds message disapper
        self.after(500,lambda:self.wrong_Answer.place_forget())




class GameLogic(Message_Display,Sound):
    '''Class for game logic'''
    def options_and_Answer_generate(self):
        '''Generate options and correct answer.'''
        start_range = 1 # starting range of number 
        end_range = 99 # End range of number
        number_of_options = 5 # Number of options(random numbers) to guess 
        self.No_of_attempts = 3 #Number of attempts available
        self.randm_number = random.sample(range(start_range,end_range+1),number_of_options) #generating the 5 random numbers 
        self.answer = random.choice(self.randm_number) #Select the correct answer from among five numbers



    def get_user_answer(self,event):
        '''Get the user's answer from the clicked button'''
        self.user_answer = event.widget.cget("text") 



    def check_guess(self):
        '''Check the user's guess'''
        self.No_of_attempts -=1 # Decrease the number of attempts by 1 after each guess
        self.show_Attempts.config(text=f"Attempts Left: {self.No_of_attempts}") # Update the label to display the remaining number of attempts
        
        if self.No_of_attempts == 0: 
            # If there are no attempts left:
            if self.answer != self.user_answer:
                # If the user's answer is not correct:   
                self.attempts_failed_sound() # Play sound for failed attempts
                self.all_attempts_failed() # Display message for all attempts failed

            else: # If the user's answer is correct:
                self.correct_answer_sound() # Play sound for correct answer
                self.correct_answer_message() # Display message for correct answer
            return

        # If there are still attempts left:
        if self.answer != self.user_answer:
            # If the user's answer is wrong
            self.wrong_answer_sound() # Play sound for wrong answer
            self.wrong_guess_message() # Display message for wrong answer.

        else:
            # If the user's answer is correct:
            self.correct_answer_sound() # Play sound for correct answer
            self.correct_answer_message() # Display message for correct answer
        



class Game_Page(GameLogic):
    '''Class for the main game page'''
    def display_options(self):
        """Display game options."""
        for window in self.winfo_children():
            window.destroy()

        self.options_and_Answer_generate() # Generate options and correct answer.

       
        frame  = Frame(background=	"#87CEFA")
        heading = Label(frame,text="Guess the correct number",font="verdana 22 normal",background=	"#87CEFA")
        heading.pack(pady=30)
        for buttons in self.randm_number:
            options = Button(frame,text=buttons,command=self.check_guess,font='helvtica 42 normal',width=3,justify='center',background="#8470FF", foreground="white")
            options.bind("<Button-1>",self.get_user_answer)
            options.pack(side=LEFT,padx=10,ipady=5,ipadx=5)
        
        frame.pack(anchor='center',expand=True)
        
        self.show_Attempts = Label(text=f"Attempts Left: {self.No_of_attempts}",font="verdana 12",foreground="white",background="#424242",width=16,height=2)
        self.show_Attempts.place(x=15,y=20)
    
        main_menu = Button(text="Main Menu",font='verdana 12 normal',background="#191970",command=self.loading_mainMenu,foreground="white")
        main_menu.bind("<Button-1>",self.click_sound)
        main_menu.pack(anchor='ne',padx=15,pady=10,ipadx=5,ipady=5)



    def loading_mainMenu(self):
        '''Display a loading message and switch to the main menu page after a delay'''
        for window in self.winfo_children():
            window.destroy()

        loading = Label(text='Loading...',font='verdana 21 normal',background="#87CEFA")
        loading.pack(anchor='center',expand=True)
        self.after(800,self.menupage)




class Menupage(Game_Page):
    '''Class for the main menu page'''

    def menupage(self):
        '''Display main menu page'''
        for window in self.winfo_children():
            window.destroy()

        menupageButtons_frame = Frame(background="#87CEFA")
        buttons = [["Start",self.loading],["Exit",(lambda:self.after(300,self.quit))]]
        for button,func in buttons:
            b = Button(menupageButtons_frame,text=button,command=func,font='verdana 22',width=15,background="#DEDEDE")
            b.bind("<Button-1>",self.click_sound)
            b.pack(anchor='nw',pady=10)
        menupageButtons_frame.pack(anchor='center',expand=True)



    def loading(self):
        '''Display a loading message and switch to the game options page after a delay'''
        for window in self.winfo_children():
            window.destroy()
        
        loading_label = Label(text="Loading...",font='verdana 21 normal',background="#87CEFA")
        loading_label.pack(anchor='center',expand=True)
        self.after(800,self.display_options)
    
    


if __name__ == "__main__":
    Game = Menupage()
    Game.menupage()
    Game.mainloop()