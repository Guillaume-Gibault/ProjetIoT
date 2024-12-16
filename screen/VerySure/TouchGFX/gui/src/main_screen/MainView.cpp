#include <gui/main_screen/MainView.hpp>
#include <cstring>


MainView::MainView() : passwordLength(0) {
    memset(passwordBuffer, 0, sizeof(passwordBuffer));
}

void MainView::setupScreen() {
    MainViewBase::setupScreen();
    Unicode::strncpy(successTextBuffer, "PASSWORD CORRECT", 20);
    Unicode::strncpy(failureTextBuffer, "PASSWORD INCORRECT", 20);
    feedbackText.invalidate(); // S'assurer que le texte s'affiche
}


void MainView::tearDownScreen()
{
    MainViewBase::tearDownScreen();
}

//Fonction permettant d'ajouter à la chaine de caracteres
void MainView::addCharacterToPassword(char c) {
    if (passwordLength < MAX_PASSWORD_LENGTH) {
        passwordBuffer[passwordLength++] = c;      // Ajoute le caractère au buffer
        passwordBuffer[passwordLength] = '\0';    // Null-terminate la chaîne
        Unicode::strncpy(passwordTextBuffer, passwordBuffer, MAX_PASSWORD_LENGTH + 1); // Met à jour le texte Unicode
        passwordText.setWildcard(passwordTextBuffer); // Lie le buffer mis à jour
        passwordText.invalidate();               // Rafraîchit l'affichage
    }
}


void MainView::removeLastCharacter() {
    if (passwordLength > 0) {
        passwordLength--;                            // Réduit la longueur du buffer
        passwordBuffer[passwordLength] = '\0';      // Null-terminate la chaîne
        Unicode::strncpy(passwordTextBuffer, passwordBuffer, MAX_PASSWORD_LENGTH + 1); // Met à jour le texte Unicode
        passwordText.setWildcard(passwordTextBuffer); // Lie le buffer mis à jour
        passwordText.invalidate();                  // Rafraîchit l'affichage
    }
}


//void MainView::validatePassword() {
//    const char* correctPassword = "GUIFERDES"; // Mot de passe correct
//    if (strcmp(passwordBuffer, correctPassword) == 0) {
//        // Afficher un message ou effectuer une action en cas de succès
//        feedbackText.setWildcard(successTextBuffer); // Mettre un texte de succès
//    } else {
//        // Afficher un message ou effectuer une action en cas d'échec
//        feedbackText.setWildcard(failureTextBuffer); // Mettre un texte d'échec
//    }
//    feedbackText.invalidate(); // Rafraîchit l'affichage du message
//}


void MainView::validatePassword() {
//    printf("Validating password: %s\n", passwordBuffer); // Débogage
    const char* correctPassword = "GUIFERDES"; // Mot de passe correct
    if (strcmp(passwordBuffer, correctPassword) == 0) {
//        printf("Password correct\n"); // Débogage
        feedbackText.setWildcard(successTextBuffer); // Mettre un texte de succès
    } else {
//        printf("Password incorrect\n"); // Débogage
        feedbackText.setWildcard(failureTextBuffer); // Mettre un texte d'échec
    }
    feedbackText.invalidate(); // Rafraîchit l'affichage du message
}



//Fonction mappant boutons ok et suppr
void MainView::buttonClicked_Suppr() {
    removeLastCharacter();
}

void MainView::buttonClicked_Ok() {
    validatePassword();
}


//Fonctions mappant les lettres
void MainView::buttonClicked_A()
{
    addCharacterToPassword('A');
}

void MainView::buttonClicked_Z()
{
    addCharacterToPassword('Z');
}

void MainView::buttonClicked_E()
{
    addCharacterToPassword('E');
}

void MainView::buttonClicked_R()
{
    addCharacterToPassword('R');
}

void MainView::buttonClicked_T()
{
    addCharacterToPassword('T');
}

void MainView::buttonClicked_Y()
{
    addCharacterToPassword('Y');
}

void MainView::buttonClicked_U()
{
    addCharacterToPassword('U');
}

void MainView::buttonClicked_I()
{
    addCharacterToPassword('I');
}

void MainView::buttonClicked_O()
{
    addCharacterToPassword('O');
}

void MainView::buttonClicked_P()
{
    addCharacterToPassword('P');
}

void MainView::buttonClicked_Q()
{
    addCharacterToPassword('Q');
}

void MainView::buttonClicked_S()
{
    addCharacterToPassword('S');
}

void MainView::buttonClicked_D()
{
    addCharacterToPassword('D');
}

void MainView::buttonClicked_F()
{
    addCharacterToPassword('F');
}

void MainView::buttonClicked_G()
{
    addCharacterToPassword('G');
}

void MainView::buttonClicked_H()
{
    addCharacterToPassword('H');
}

void MainView::buttonClicked_J()
{
    addCharacterToPassword('J');
}

void MainView::buttonClicked_K()
{
    addCharacterToPassword('K');
}

void MainView::buttonClicked_L()
{
    addCharacterToPassword('L');
}

void MainView::buttonClicked_M()
{
    addCharacterToPassword('M');
}

void MainView::buttonClicked_W()
{
    addCharacterToPassword('W');
}

void MainView::buttonClicked_X()
{
    addCharacterToPassword('X');
}

void MainView::buttonClicked_C()
{
    addCharacterToPassword('C');
}

void MainView::buttonClicked_V()
{
    addCharacterToPassword('V');
}

void MainView::buttonClicked_B()
{
    addCharacterToPassword('B');
}

void MainView::buttonClicked_N()
{
    addCharacterToPassword('N');
}
