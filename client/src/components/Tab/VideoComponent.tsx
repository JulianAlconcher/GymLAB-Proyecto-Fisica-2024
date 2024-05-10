import React from 'react'



interface VideoComponentProps {
   videoRef : React.MutableRefObject<HTMLVideoElement | null>;
}



export default function VideoComponent(props : VideoComponentProps) {

    
  return (
    <video className="m-2" ref={props.videoRef} controls autoPlay />

  )
}
