.. _exp-mobile-a11y-basics:

########################################################
Basic Principles of Accessibility in Mobile Applications
########################################################

When creating an accessible mobile application, many aspects, such as methods of presenting information, can follow the same principles as Web accessibility.
This section explains the basic principles specific to mobile application accessibility.

***************************************************
Avoid Creating Application-Specific Custom Gestures
***************************************************

To ensure that users who rely on assistive technologies, such as screen readers or switch interfaces, can operate a mobile application, all features of the application must be accessible through the standard gestures provided by the mobile OS.
Standard gestures are designed with accessibility in mind, and corresponding methods of operation are defined when assistive technologies are in use.
For example, a standard tap gesture can be executed with a double tap when a screen reader is in use.
As such, standard gestures have high compatibility with assistive technologies, ensuring that all users can interact with the application without frustration.

On the other hand, custom gestures implemented within the application may not be recognized correctly by assistive technologies and may not work in certain usage environments.
Furthermore, users must learn and master such gestures, making the application less user-friendly.

Therefore, all features offered by the application must be accessible using standard mobile OS gestures.
While there is no problem in offering custom gestures themselves, functions that depend solely on such gestures for use should not be created.

Standard Gestures for User Interaction
======================================

The standard gestures provided by mobile OSs are extensive, with many available methods of interaction, but most users do not know all of them. Therefore, when considering accessibility, it is important to design the interface around simple and intuitive interactions.

In particular, when a screen reader is enabled, it is recommended to design the application so that all information can be accessed and all functions can be executed using only basic gestures, such as a one-finger left/right flick and a one-finger double tap. This approach allows users to operate the application smoothly without needing to learn additional or complex gestures.

Additionally, in situations where the screen reader is disabled, it is safe to base interactions on gestures that most users are already familiar with, such as taps and long presses. This not only makes the application easier to use for non-assistive technology users, but also often leads to improved accessibility when assistive technologies are in use. These simple interactions can be easily recognized by assistive technologies, maintaining consistency in user experience, which ultimately contributes to overall accessibility improvements.

Of course, there is no issue with using other standard gestures as well. However, it is important to share a clear understanding within the development team of which gestures will be supported, and to ensure consistency in UI design. A lack of consistency in the UI can lead to confusion, especially for users relying on assistive technologies or those unfamiliar with gestures.

****************************************
Ensure Compatibility with Screen Readers
****************************************

Ensuring that all functions can be operated without issues using a screen reader is a critical aspect of mobile application accessibility.
This is because making the application accessible to screen reader users generally makes it easier to operate for users of many other assistive technologies as well.

For example, if components can be correctly focused using a screen reader, users of switch interfaces will also be able to access those components easily.
Similarly, if all interface elements on the screen are read out correctly by the screen reader, users who rely on voice recognition to operate the application will also be able to specify those components and give the necessary commands.

**********************************
When Custom Gestures Are Essential
**********************************

There are cases where the use of custom gestures is essential, such as when requiring a handwritten signature.
However, even in such cases, it is important to first consider whether there are alternative ways to achieve the same purpose without relying on such implementations.

If custom gestures remain indispensable, it is necessary to implement them in a way that ensures they can still be operated smoothly when assistive technologies are in use.

.. include:: /inc/info2gl/exp-mobile-a11y-basics.rst
