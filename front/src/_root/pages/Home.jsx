import { useAuth } from '@/context/AuthContext';

const Home = () => {
  const { isLoggedIn } = useAuth();

  if (!isLoggedIn) {
    return <div></div>;
  }

  return (
    <div>
    </div>
  )
}

export default Home