import React from 'react'



interface VideoComponentProps {
   videoRef : React.MutableRefObject<HTMLVideoElement | null>;
}



export default function VideoComponent(props : VideoComponentProps) {

    
  return (
    <video className="m-2 border-2 border-black rounded-md w-full " ref={props.videoRef} controls autoPlay />

  )
}
