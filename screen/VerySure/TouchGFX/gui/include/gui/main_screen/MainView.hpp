#ifndef MAINVIEW_HPP
#define MAINVIEW_HPP

#include <gui_generated/main_screen/MainViewBase.hpp>
#include <gui/main_screen/MainPresenter.hpp>

class MainView : public MainViewBase
{
public:
    MainView();
    virtual ~MainView() {}
    virtual void setupScreen();
    virtual void tearDownScreen();

    //Fonction des boutons
    virtual void buttonClicked_A();
    virtual void buttonClicked_Z();
    virtual void buttonClicked_E();
    virtual void buttonClicked_R();
    virtual void buttonClicked_T();
    virtual void buttonClicked_Y();
    virtual void buttonClicked_U();
    virtual void buttonClicked_I();
    virtual void buttonClicked_O();
    virtual void buttonClicked_P();
    virtual void buttonClicked_Q();
    virtual void buttonClicked_S();
    virtual void buttonClicked_D();
    virtual void buttonClicked_F();
    virtual void buttonClicked_G();
    virtual void buttonClicked_H();
    virtual void buttonClicked_J();
    virtual void buttonClicked_K();
    virtual void buttonClicked_L();
    virtual void buttonClicked_M();
    virtual void buttonClicked_W();
    virtual void buttonClicked_X();
    virtual void buttonClicked_C();
    virtual void buttonClicked_V();
    virtual void buttonClicked_B();
    virtual void buttonClicked_N();

protected:
    // Buffer pour le texte du mot de passe
    static constexpr uint8_t MAX_PASSWORD_LENGTH = 20;
    char passwordBuffer[MAX_PASSWORD_LENGTH + 1] = "";
    uint8_t passwordLength = 0;

        // Fonction utilitaire pour ajouter un caractère
    void addCharacterToPassword(char c);
    void removeLastCharacter();
    void validatePassword();
};

#endif // MAINVIEW_HPP
