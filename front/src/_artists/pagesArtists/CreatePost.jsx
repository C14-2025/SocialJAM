import PostForms from '@/components/forms/PostForms'

const CreatePost = () => {
  return (
    <div className='flex-1 flex'>

      <div className='common-container'>

        <div className='max-w-5x1 flex-start gap-3 justify-start w-full'>

          <img 

            src="/assets/icons/add-post.svg"
            width={36}
            height={36}
            alt="adicionar post"
          
          />

          <h2 className='text-2xl font-semibold'>Criar novo post</h2>

        </div>

        <PostForms />

      </div>

    </div>
  )
}

export default CreatePost