import { SignUp, SignIn, ResetPasswordPage, PasswordConfirmation, NewPasswordPage, EmailConfirmation } from './components/auth.jsx';
import { HomePage, ResourceUploadPage } from './components/resources.jsx';
import { ChatPage } from './components/chat.jsx';
import { LandingPage } from './components/landing.jsx';

const routes = [
    {
      path: '/',
      element: <LandingPage />,
    },
    {
      path: '/home',
      element: <HomePage />,
    },
    {
      path: '/sign-in',
      element: <SignIn />,
    },
    {
      path: '/sign-up',
      element: <SignUp />,
    },
    {
      path: '/confirm-account/:status',
      element: <EmailConfirmation />,
    },
    {
      path: '/password-confirmation/:status',
      element: <PasswordConfirmation />
    },
    {
      path: '/chats',
      element: <ChatPage />,
    },
    {
      path: '/upload-resource',
      element: <ResourceUploadPage />,
    },
    {
      path: '/reset-password',
      element: <ResetPasswordPage />,
    },
    {
      path: '/create-password',
      element: <NewPasswordPage />,
    },
]

export { routes };
