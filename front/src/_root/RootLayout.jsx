import { Outlet } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';

const RootLayout = () => {
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <div>
      <header>
        <Button onClick={handleLogout}>
          Sair
        </Button>
      </header>
      
      <main className="flex-1 flex">
        <Outlet />
      </main>
    </div>
  )
}

export default RootLayout