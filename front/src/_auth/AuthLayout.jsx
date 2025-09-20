import {Outlet, Navigate} from "react-router-dom"
import { useAuth } from '@/context/AuthContext';

const AuthLayout = () => {
  const { isLoggedIn, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex-center w-full h-screen">
        <div className="flex-center gap-2">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
          Carregando...
        </div>
      </div>
    );
  }

  return (
    <>
      {isLoggedIn ? (
          <Navigate to="/" />
        ):(
          <>
            <section className="flex flex-1 justify-center items-center flex-col py-10">
              <Outlet />
            </section>
            <img
              src="/assets/images/Fundo_teste_02.png"
              alt="logo"
              className="hidden md:block w-1/2 object-cover bg-no-repeat"
            />

          </>
        )
      }  
    </>
  )
}

export default AuthLayout