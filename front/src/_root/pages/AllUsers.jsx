import { InputGroup, InputGroupInput, InputGroupAddon, InputGroupButton } from '@/components/ui/input-group'
import { Button } from '@/components/ui/button'
import React, { useState, useEffect } from 'react'
import { searchUsers, sendFriendRequest, getSentFriendRequests, getFriends, getReceivedFriendRequests, respondToFriendRequest, getMe } from '@/api'
import { useAuth } from '@/context/AuthContext';
import { useNavigate, useParams } from 'react-router-dom'
import CardUser from '@/components/shared/CardUser'

const AllUsers = () => {
  const [searchValue, setSearchValue] = useState('')
  const [users, setUsers] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const [sentRequests, setSentRequests] = useState([])
  const [receivedRequests, setReceivedRequests] = useState([])
  const [friends, setFriends] = useState([])
  const [buttonLoading, setButtonLoading] = useState(false)
  const [currentUser, setCurrentUser] = useState(null)
  const navigate = useNavigate()
  const { username } = useParams()

  const handleUserClick = (user) => {
    if (currentUser && user.username === currentUser.username) {
      return
    }
    setSelectedUser(user)
    navigate(`/all-users/${user.username}`)
  }

  const handleBackToSearch = () => {
    setSelectedUser(null)
    navigate('/all-users')
  }

  const handleSendRequest = async (userId) => {
    setButtonLoading(true)
    const result = await sendFriendRequest(userId)
    
    if (result.success) {
      //atualiza a lista de solicitações enviadas
      setSentRequests(prev => [...prev, result.data])
    } else {
      alert(result.error)
    }
    
    setButtonLoading(false)
  }

  const handleAcceptRequest = async (requestId) => {
    setButtonLoading(true)
    const result = await respondToFriendRequest(requestId, 'accepted')
    
    if (result.success) {
      //remove da lista de recebidas e adiciona aos amigos
      setReceivedRequests(prev => prev.filter(req => req.id !== requestId))
      //recarrega amigos
      const friendsResult = await getFriends()
      if (friendsResult.success) {
        setFriends(friendsResult.data)
      }
    } else {
      alert(result.error)
    }
    
    setButtonLoading(false)
  }


  useEffect(() => {
    const fetchCurrentUser = async () => {
      const result = await getMe()
      if (result.success) {
        setCurrentUser(result.me)
      }
    }
    fetchCurrentUser()
  }, [])

  //busca solicitações enviadas e amigs ao carregar
  useEffect(() => {
    const fetchRequestsAndFriends = async () => {
      const [sentResult, receivedResult, friendsResult] = await Promise.all([
        getSentFriendRequests(),
        getReceivedFriendRequests(),
        getFriends()
      ])
      
      if (sentResult.success) {
        setSentRequests(sentResult.data)
      }
      
      if (receivedResult.success) {
        setReceivedRequests(receivedResult.data)
      }
      
      if (friendsResult.success) {
        setFriends(friendsResult.data)
      }
    }
    
    fetchRequestsAndFriends()
  }, [])

  useEffect(() => {
    if (username && users.length > 0 && currentUser) {
      // Impede acesso ao próprio perfil pela URL
      if (username === currentUser.username) {
        navigate('/all-users')
        return
      }
      const user = users.find(u => u.username === username)
      if (user) {
        setSelectedUser(user)
      }
    } else if (!username) {
      setSelectedUser(null)
    }
  }, [username, users, currentUser, navigate])

  
  useEffect(() => {
    const fetchUsers = async () => {
      setIsLoading(true) 
      
      const result = await searchUsers(searchValue) //aqui ele vai pegar o valor do searchValue lá de baixo

      if(result.success){
        console.log('Usuários encontrados:', result.users) 
        const filteredUsers = currentUser 
          ? result.users.filter(user => user.username !== currentUser.username)
          : result.users
        setUsers(filteredUsers) //se achar vai setar o user
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
    const isFriend = friends.some(friend => friend.id === selectedUser.id)
    const requestSent = sentRequests.some(request => request.receiver_id === selectedUser.id)
    const requestReceived = receivedRequests.find(request => request.sender_id === selectedUser.id)
    
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
          
          {isFriend ? (
            <Button 
              size="lg"
              disabled
              className="w-80 py-6 rounded-2xl bg-primary-500 text-light-1 opacity-50 cursor-not-allowed hover:bg-primary-500"
            >
              <svg 
                className="w-5 h-5 mr-2" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M5 13l4 4L19 7" 
                />
              </svg>
              Vocês já são amigos
            </Button>
          ) : requestReceived ? (
            <Button 
              size="lg"
              onClick={() => handleAcceptRequest(requestReceived.id)}
              disabled={buttonLoading}
              className="w-80 py-6 rounded-2xl bg-green-600 hover:bg-green-700 text-white transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:hover:scale-100"
            >
              {buttonLoading ? (
                <img src="../../assets/icons/loader.svg" alt="Carregando" className="w-5 h-5" />
              ) : (
                <>
                  <svg 
                    className="w-5 h-5 mr-2" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={2} 
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" 
                    />
                  </svg>
                  Aceitar pedido de amizade
                </>
              )}
            </Button>
          ) : requestSent ? (
            <Button 
              size="lg"
              disabled
              className="w-80 py-6 rounded-2xl bg-dark-4 text-light-1 cursor-not-allowed hover:bg-dark-4"
            >
              <svg 
                className="w-5 h-5 mr-2" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" 
                />
              </svg>
              Solicitação enviada
            </Button>
          ) : (
            <Button 
              size="lg"
              onClick={() => handleSendRequest(selectedUser.id)}
              disabled={buttonLoading}
              className="w-80 py-6 rounded-2xl bg-primary-500 text-light-1 transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:hover:scale-100"
            >
              {buttonLoading ? (
                <img src="../../assets/icons/loader.svg" alt="Carregando" className="w-5 h-5" />
              ) : (
                <>
                  <svg 
                    className="w-5 h-5 mr-2" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={2} 
                      d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" 
                    />
                  </svg>
                  Enviar solicitação de amizade
                </>
              )}
            </Button>
          )}
          
        </div>
      </div>
    )
  }

  //caso contrário, mostra a busca
  return (
    <div className="flex flex-1 min-h-screen bg-exploreusers bg-fixed">
      <div className="common-container">
        <div className="user-container">
          <h2 className="h3-bold md:h2-bold text-left w-full">Busque por usuários</h2>
          
          
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