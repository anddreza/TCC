import { Button } from 'antd';
import { useState } from 'react';

export const Photos = (props) => {
    const [activeIndex, setActiveIndex] = useState(0)
    const nextPhoto = () => {
        const newIndex = activeIndex + 1;
        if (newIndex >= props.photosList.length) {
            setActiveIndex(0);
        } else {
            setActiveIndex(newIndex);
        }
    }

    const previousPhoto = () => {
        const newIndex = activeIndex - 1;
        if (newIndex < 0) {
            setActiveIndex(props.photosList.length - 1);
        } else {
            setActiveIndex(newIndex);
        }
    }

    return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', flexDirection: 'column' }}>
            <img
                style={{ maxWidth: '350px', borderRadius: '8px' }}
                src={props.photosList[activeIndex].url} alt="Property Photo" />
            <div style={{}}>
                <Button onClick={previousPhoto} type="primary" shape="circle">{"<"}</Button>
                <Button onClick={nextPhoto} type="primary" shape="circle">{">"}</Button>
            </div>
        </div>
    )
}