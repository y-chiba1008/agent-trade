import { createBrowserRouter } from 'react-router'
import { AppLayout } from '@/components/layout/appLayout'
import { AccountDetailPage } from '@/features/account/detail/accountDetailPage'
import { AccountListPage } from '@/features/account/list/accountListPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <AccountListPage />,
      },
      {
        path: 'accounts/:accountId',
        element: <AccountDetailPage />,
      },
    ],
  },
])
