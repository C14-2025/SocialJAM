import { InputGroup, InputGroupInput, InputGroupAddon, InputGroupButton } from '@/components/ui/input-group'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import React, { useState, useEffect } from 'react'
import { searchUsers, sendFriendRequest, getSentFriendRequests, getFriends, getReceivedFriendRequests, respondToFriendRequest, getMe, removeFriend, getUserById } from '@/api'
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
  const [showOnlyFriends, setShowOnlyFriends] = useState(false)
  const [activeTab, setActiveTab] = useState('search') // 'search' ou 'requests'
  const navigate = useNavigate()
  const { username } = useParams()
  const hasSearch = searchValue.trim().length > 0;
  const hasResults = users.length > 0;


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

  const handleDeclineRequest = async (requestId) => {
    setButtonLoading(true)
    const result = await respondToFriendRequest(requestId, 'denied')
    
    if (result.success) {
      //remove da lista de recebidas
      setReceivedRequests(prev => prev.filter(req => req.id !== requestId))
    } else {
      alert(result.error)
    }
    
    setButtonLoading(false)
  }

  const handleRemoveFriend = async (friendId) => {
    
    setButtonLoading(true)
    const result = await removeFriend(friendId)
    
    if (result.success) {
      //remove da lista de amigos
      setFriends(prev => prev.filter(friend => friend.id !== friendId))
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
        //busca dados completos de cada sender
        const requestsWithSenders = await Promise.all(
          receivedResult.data.map(async (request) => {
            try {
              //busca o usuário pelo ID do sender
              const senderData = await getUserById(request.sender_id)
              return { 
                ...request, 
                sender: senderData.success ? senderData.data : null 
              }
            } catch (error) {
              console.error(`Erro ao buscar sender ${request.sender_id}:`, error)
              return { ...request, sender: null }
            }
          })
        )
        setReceivedRequests(requestsWithSenders)
      }
      
      if (friendsResult.success) {
        setFriends(friendsResult.data)
      }
    }
    
    fetchRequestsAndFriends()
  }, [])

  useEffect(() => {
    if (username && users.length > 0 && currentUser) {
      //impede acesso ao próprio perfil pela URL
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
      
      if (showOnlyFriends) {
        //filtra amigos pela busca
        const filteredFriends = friends.filter(friend => 
          friend.username?.toLowerCase().includes(searchValue.toLowerCase()) ||
          friend.nome?.toLowerCase().includes(searchValue.toLowerCase()) ||
          friend.favorite_artist?.toLowerCase().includes(searchValue.toLowerCase())
        )
        setUsers(filteredFriends)
        setIsLoading(false)
      } else {
        const result = await searchUsers(searchValue)

        if(result.success){
          const filteredUsers = currentUser 
            ? result.users.filter(user => user.username !== currentUser.username)
            : result.users
          setUsers(filteredUsers)
        } else {
          console.error('Erro:', result.error)
          setUsers([])
        }
        
        setIsLoading(false)
      }
    }

    
    const timeoutId = setTimeout(() => {
      fetchUsers()
    }, 500) 

    return () => clearTimeout(timeoutId)
  }, [searchValue, showOnlyFriends, friends, currentUser])

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
            <div className="flex flex-col gap-3 items-center justify-center w-full max-w-2xl mx-auto">
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
              <Button
                variant="ghost"
                onClick={() => handleRemoveFriend(selectedUser.id)}
                disabled={buttonLoading}
                className="text-red-400 hover:text-red-300 hover:bg-red-950/20 transition-colors"
              >
                <svg 
                  className="w-4 h-4 mr-2" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M13 7a4 4 0 11-8 0 4 4 0 018 0zM9 14a6 6 0 00-6 6v1h12v-1a6 6 0 00-6-6zM21 12h-6" 
                  />
                </svg>
                Desfazer amizade
              </Button>
            </div>
          ) : requestReceived ? (
            <div className="flex flex-col gap-3 items-center justify-center w-full max-w-2xl mx-auto">
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
              <Button
                variant="ghost"
                onClick={() => handleDeclineRequest(requestReceived.id)}
                disabled={buttonLoading}
                className="text-red-400 hover:text-red-300 hover:bg-red-950/20 transition-colors"
              >
                <svg 
                  className="w-4 h-4 mr-2" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M6 18L18 6M6 6l12 12" 
                  />
                </svg>
                Recusar pedido
              </Button>
            </div>
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
    <div className={`flex flex-1 min-h-screen bg-dark-1 bg-fixed ${hasSearch || showOnlyFriends || activeTab === 'requests' ? "" : "bg-exploreusers"}`}>
      <div className="common-container">
        <div className="user-container">
          {/* abas */}
          <div className="flex gap-4 mb-6 border-b border-dark-4">
            <button
              onClick={() => setActiveTab('search')}
              className={`px-6 py-3 font-semibold transition-all ${
                activeTab === 'search'
                  ? 'text-primary-500 border-b-2 border-primary-500'
                  : 'text-light-3 hover:text-light-1'
              }`}
            >
              Buscar Usuários
            </button>
            <button
              onClick={() => setActiveTab('requests')}
              className={`px-6 py-3 font-semibold transition-all relative ${
                activeTab === 'requests'
                  ? 'text-primary-500 border-b-2 border-primary-500'
                  : 'text-light-3 hover:text-light-1'
              }`}
            >
              Solicitações
              {receivedRequests.length > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-600 text-white text-xs rounded-full flex items-center justify-center">
                  {receivedRequests.length}
                </span>
              )}
            </button>
          </div>

          {activeTab === 'search' ? (
            <>
              <div className="flex items-center justify-between w-full mb-6">
                <h2 className="h3-bold md:h2-bold text-left">{showOnlyFriends ? 'Seus Amigos' : 'Busque por usuários'}</h2>
                <div className="flex items-center gap-3">
                  <span className="text-light-2 small-medium">Mostrar apenas amigos</span>
                  <Switch 
                    checked={showOnlyFriends}
                    onCheckedChange={setShowOnlyFriends}
                    className="data-[state=checked]:bg-primary-500"
                  />
                </div>
              </div>
          
          <InputGroup className="w-full max-w-5xl bg-dark-4 rounded-xl border-2 border-transparent focus-within:border-white transition-colors">
            <InputGroupInput 
              placeholder={showOnlyFriends ? "Busque amigos" : "Busque usuários"} 
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
            </>
          ) : (
            // aba de Solicitações 
            <div className="w-full max-w-4xl mx-auto">
              <h2 className="h3-bold md:h2-bold text-left mb-6">Solicitações de Amizade</h2>
              
              {receivedRequests.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <svg 
                    className="w-20 h-20 text-light-4 mb-4 opacity-50" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={2} 
                      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" 
                    />
                  </svg>
                  <p className="text-light-3 text-lg">Nenhuma solicitação pendente</p>
                </div>
              ) : (
                <div className="flex flex-col gap-4">
                  {receivedRequests.map((request) => (
                    <div 
                      key={request.id}
                      className="bg-dark-3 rounded-xl p-6 flex items-center justify-between hover:bg-dark-4 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <img 
                          src={request.sender?.user_photo_url ? `http://localhost:8000/${request.sender.user_photo_url}` : '/assets/icons/profile-placeholder.svg'}
                          alt={request.sender?.username}
                          className="w-16 h-16 rounded-full object-cover"
                        />
                        <div>
                          <p className="base-semibold text-light-1">{request.sender?.username}</p>
                          <p className="small-regular text-light-3">{request.sender?.favorite_artist || 'Sem artista favorito'}</p>
                        </div>
                      </div>
                      
                      <div className="flex gap-3">
                        <Button
                          onClick={() => handleAcceptRequest(request.id)}
                          disabled={buttonLoading}
                          className="bg-green-600 hover:bg-green-700 text-white transition-all disabled:opacity-50"
                        >
                          {buttonLoading ? (
                            <img src="/assets/icons/loader.svg" alt="Carregando" className="w-5 h-5" />
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
                                  d="M5 13l4 4L19 7" 
                                />
                              </svg>
                              Aceitar
                            </>
                          )}
                        </Button>
                        
                        <Button
                          variant="ghost"
                          onClick={() => handleDeclineRequest(request.id)}
                          disabled={buttonLoading}
                          className="text-red-400 hover:text-red-300 hover:bg-red-950/20 transition-colors"
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
                              d="M6 18L18 6M6 6l12 12" 
                            />
                          </svg>
                          Recusar
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AllUsers