
# UI beginning Scripts for PyQt5/QML - PyQtLauncher -

In many ways, when I want to start a project, I need a UI. This repo gives me a basis to speed it up.

    I. The root Dir contains all necessary for standard PyQt5 UI.
        Step 1:
            - Open the Qt designer file (extension '.ui').
            - Build it as a wireframe.
            - A '.qrc' resource file is already linked to the design and already contains some icons, which are also stored in 'icon' folder.
        Step 2:
            - The ui.py contains the main UI class and is the entry point to run first.
            - Running it will automatically generate ui and resource python file and import them.
        Step 3:
            - The worker.py is imported in ui.py and the execution of the class inside is moved to a dedicated QTread.
            - Code your app functionality in the worker and link the worker signals from the main thread (MainUI class) to the appropriate UI widget.

    II. The QML Dir contains a special mechanism to speed up QML apps.
        Step 1:
            - The '.qml' file contains the UI declarative language of Qt. 
        Step 2:
            - Running startProject is the entry point of the qml app. It will detect automatically '.qml', '.png' and build the '.qmldir' and the '.qrc' tree files with links. 
        Step 3:
            - Implement a 'ComStructGen' function that speeds up the creation of a QObject interface, creating a setter and getter, an associated property and linking a notification signal for each given variable. It declares the generated class in globals, creates one instance, registers it in the context properties and returns the instance.