import { useAuth } from '@/context/AuthContext';

const Home = () => {
  const { isLoggedIn } = useAuth();

  if (!isLoggedIn) {
    return <div>Acesso negado</div>;
  }

  return (
    <div>
      <h1>Bem-vindo ao SocialJAM!</h1>
      <p>Você está logado com sucesso.</p>
    </div>
  )
}

export default Home