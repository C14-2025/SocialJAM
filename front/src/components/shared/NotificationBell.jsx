import { useState, useEffect, useRef } from 'react';
import { getNotifications, markNotificationAsRead } from '@/api';
import { Bell } from 'lucide-react';

const NotificationBell = () => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const dropdownRef = useRef(null);

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const response = await getNotifications();
      console.log('Notificações recebidas:', response);
      if (response.success) {
        setNotifications(response.data);
        const unread = response.data.filter(n => !n.read).length; //Aqui ele filtra tudo que não foi lido
        setUnreadCount(unread);
      }
    } catch (error) {
      console.error('Erro ao buscar notificações:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log('NotificationBell montado');
    fetchNotifications();
    
    // a cada 30 seg vai atualizar sozinho
    const interval = setInterval(fetchNotifications, 30000);
    
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) { //troca o estado do dropdown ref ao clicar fora
        setIsOpen(false);
      }
    };

    if (isOpen) { //se estiver aberto ele faz a logica do clique fora
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside); //depois limpa
    };
  }, [isOpen]); //toda vez que o estado de is open muda

  const handleMarkAsRead = async (notificationId) => {
    try {
      const response = await markNotificationAsRead(notificationId);
      if (response.success) {
        setNotifications(prev => 
          prev.map(n => n.id === notificationId ? { ...n, read: true } : n) //aqui ele filtra pelo id e se for igual
        );                                                               //ele troca o read pra true, se n deixa do mesmo jeito
        setUnreadCount(prev => Math.max(0, prev - 1)); //conta quantos estão sendo lidos
      }
    } catch (error) {
      console.error('Erro ao marcar notificação como lida:', error);
    }
  };

  const formatTime = (dateString) => { //função pra formatar a data e o tempo
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);

    if (diffInSeconds < 60) return 'Agora';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m atrás`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h atrás`;
    return `${Math.floor(diffInSeconds / 86400)}d atrás`;
  };

  return (
    <div className="relative w-full" ref={dropdownRef}>
      <button
        onClick={async () => {
          //marca todas as notificações não lidas como lidas
          if (!isOpen && unreadCount > 0) {
            const unreadNotifications = notifications.filter(n => !n.read);
            for (const notification of unreadNotifications) {
              await markNotificationAsRead(notification.id);
            }
          }
          
          setIsOpen(!isOpen);
        }}
        className="group relative flex items-center gap-4 p-4 w-full rounded-[10px] hover:bg-primary-500 transition-all"
        aria-label="Notificações"
      >
        <div className="relative">
          <Bell className="w-6 h-6 text-primary-500 group-hover:invert-white transition-all" />
          
          {/* aqui se n estiver zerado a quantidade de coisa lida ele faz a bolinha aparecer  */}
          {unreadCount > 0 && (
            <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-primary-500 rounded-full animate-pulse"></span>
          )}
        </div>
        
        <span className="text-light-1 group-hover:text-white transition-all">
          Notificações
        </span>
      </button>

      
      {isOpen && (
        <div className="fixed left-[270px] bottom-[80px] w-80 bg-dark-3 border-2 border-primary-500 rounded-xl shadow-2xl z-[9999] max-h-96 overflow-hidden flex flex-col">
          <div className="px-5 py-4 bg-dark-2 border-b border-dark-4">
            <h3 className="text-light-1 font-bold text-lg">Notificações</h3>
          </div>

          
          <div className="overflow-y-auto flex-1 bg-dark-2">
            {loading ? (
              <div className="flex items-center justify-center py-10">
                <div className="w-8 h-8 border-3 border-primary-500 border-t-transparent rounded-full animate-spin" />
              </div>
            ) : notifications.length === 0 ? (
              <div className="px-5 py-10 text-center">
                <Bell className="w-12 h-12 text-light-4 mx-auto mb-3 opacity-50" />
                <p className="text-light-3 font-medium">Nenhuma notificação</p>
              </div>
            ) : (
              <div>
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    onClick={() => !notification.read && handleMarkAsRead(notification.id)}
                    className={`px-5 py-4 cursor-pointer transition-all hover:bg-dark-4 border-b border-dark-4 last:border-b-0 ${
                      !notification.read ? 'bg-dark-3' : ''
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      
                      {!notification.read && (
                        <div className="w-3 h-3 bg-primary-500 rounded-full mt-1 flex-shrink-0 animate-pulse" />
                      )}
                      
                      <div className="flex-1 min-w-0">
                        <p className={`text-sm leading-relaxed ${!notification.read ? 'text-light-1 font-semibold' : 'text-light-3'}`}>
                          {notification.content}
                        </p>
                        <p className="text-xs text-primary-500 mt-2 font-medium">
                          {formatTime(notification.created_at)}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          
          {notifications.length > 0 && (
            <div className="px-5 py-3 bg-dark-2 border-t-2 border-dark-4">
              <button
                onClick={() => {
                  fetchNotifications();
                }}
                className="text-sm text-primary-500 hover:text-white hover:bg-primary-500 font-semibold w-full text-center py-2 rounded-lg transition-all"
              >
                Atualizar
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationBell;
