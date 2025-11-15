import { InputGroup, InputGroupInput, InputGroupAddon, InputGroupButton } from '@/components/ui/input-group'
import React, { useState, useEffect } from 'react'
import { searchUsers } from '@/api'
import { useNavigate, useParams } from 'react-router-dom'
import CardUser from '@/components/shared/CardUser'

const AllUsers = () => {
  const [searchValue, setSearchValue] = useState('')
  const [users, setUsers] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const navigate = useNavigate()
  const { username } = useParams()

  const handleUserClick = (user) => {
    setSelectedUser(user)
    navigate(`/all-users/${user.username}`)
  }

  const handleBackToSearch = () => {
    setSelectedUser(null)
    navigate('/all-users')
  }


  useEffect(() => {
    if (username && users.length > 0) {
      const user = users.find(u => u.username === username)
      if (user) {
        setSelectedUser(user)
      }
    } else if (!username) {
      setSelectedUser(null)
    }
  }, [username, users])

  
  useEffect(() => {
    const fetchUsers = async () => {
      setIsLoading(true) 
      
      const result = await searchUsers(searchValue) //aqui ele vai pegar o valor do searchValue lá de baixo

      if(result.success){
        console.log('Usuários encontrados:', result.users) 
        setUsers(result.users) //se achar vai setar o user
      } else {
        console.error('Erro:', result.error) //se der erro vai mandar um array vazio
        setUsers([])
      }
      
      setIsLoading(false)
    }

    
    const timeoutId = setTimeout(() => {
      fetchUsers()
    }, 500) 

    return () => clearTimeout(timeoutId)
  }, [searchValue]) //executa sempre que searchValue mudar

  //se tiver username na url e usuário selecionado, mostra o perfil
  if (username && selectedUser) {
    return (
      <div className="flex flex-1">
        <div className="common-container">
          <button 
            onClick={handleBackToSearch}
            className="flex items-center gap-2 text-light-3 hover:text-light-1 transition-colors mb-4"
          >
            <img 
              src="/assets/icons/back.svg" 
              alt="Voltar" 
              className="w-6 h-6"
            />
            Voltar para busca
          </button>
          <CardUser 
            image={selectedUser.user_photo_url ? `http://localhost:8000/${selectedUser.user_photo_url}` : null}
            nomeUsuario={selectedUser.username} 
            artistaFav={selectedUser.favorite_artist || 'Não informado'} 
          />
        </div>
      </div>
    )
  }

  // Caso contrário, mostra a busca
  return (
    <div className="flex flex-1 min-h-screen bg-exploreusers bg-fixed">
      <div className="common-container">
        <div className="user-container">
          <h2 className="h3-bold md:h2-bold text-left w-full">All Users</h2>
          
          <InputGroup className="w-full max-w-5xl bg-dark-4 rounded-xl border-2 border-transparent focus-within:border-white transition-colors">
            <InputGroupInput 
              placeholder="Busque usuários" 
              className="h-12 bg-transparent border-none placeholder:text-light-4 focus-visible:ring-0 focus-visible:ring-offset-0 text-light-1"
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
            />
          </InputGroup>

          {isLoading && (
            <div className="flex-center w-full">
              <img src="../../assets/icons/loader.svg" alt="Carregando" />
            </div>
          )}

          <div className="user-grid">
            
            

            {!isLoading && users.length > 0 && users.map((user, index) => (
              <div 
                key={user.id || user.username} 
                className="bg-dark-3 rounded-2xl cursor-pointer transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-xl p-4 animate-in fade-in"
                style={{ 
                  animationDelay: `${index * 50}ms`,
                  animationDuration: '400ms',
                  animationFillMode: 'backwards'
                }}
                onClick={() => handleUserClick(user)}
              >
                <div className="flex flex-col items-center gap-2">
                  <img 
                    src={user.user_photo_url ? `http://localhost:8000/${user.user_photo_url}` : '/assets/icons/profile-placeholder.svg'} 
                    alt={user.username}
                    className="w-24 h-24 rounded-full object-cover"
                  />
                  <div className="text-center">
                    <p className="base-medium text-light-1 line-clamp-1">{user.username}</p>
                    <p className="small-regular text-light-3 line-clamp-1">{user.favorite_artist || "sem artista favorito"}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AllUsers