import gamestate

def menu_main():
    
    print('\n--------------------------------------------------------\n')
    print('Main Menu:\n')
    print('\t1) Start playing.')
    print('\t2) Configuration.')
    print('\t3) Exit.\n')

    return input('Option: ')

def menu_config():

    print('\n--------------------------------------------------------\n')
    print('\t1) Add solutions.')
    print('\t2) View solution.')
    print('\t3) Save database.')
    print('\t4) Reload database.')
    print('\t5) Back to Main Menu.\n')

    return input('Option: ')


# load database

# <load database>

# main menu

state_main = True
state_config = False

print('Database loaded.')

while(state_main): 

    selection = menu_main()

    if selection == '1': # Start playing

        print('\nRunning...')

    elif selection == '2': # Configuration

        state_config = True

        while(state_config):

            selection = menu_config()

            if selection == '1': # Add solutions
        
                print('\nAdding Solutions...\n')
        
            elif selection == '2': # View solution
        
                print('\nViewing Solution...\n')
        
            elif selection == '3': # Save database
        
                print('\nSaving Database...\n')
        
            elif selection == '4': # Reload database
        
                print('\nReloading Database...\n')

            elif selection == '5': # Return to main menu

                print('\nReturning to Main Menu...')
                state_config = False
        
            else: # Invalid input
                print('\nInvalid Input. Try again.\n')

    elif selection == '3': # Exit

        #exit

        print('\nExiting...')
        state_main = False

    else: # Invalid input
        print('\nInvalid Input. Try again.\n')