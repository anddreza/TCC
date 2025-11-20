import React from 'react';
import { Button, Form, Input } from 'antd';

const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};



export const TextSearchBox = (props) => { 
    const handleSubmit = ({ Prompt }) => props.onSubmit(Prompt);

    return (
        <Form
            name="basic"
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 16 }}
            style={{ maxWidth: 600 }}
            initialValues={{ remember: true }}
            onFinish={handleSubmit}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
        >
            <Form.Item
            label="Search"
            name="Prompt"
            rules={[{ required: true, message: 'Please insert type your ideal apart' }]}
            >
            <Input />
            </Form.Item>

            <Form.Item label={null}>
            <Button type="primary" htmlType="submit">
                Pesquisar
            </Button>
            </Form.Item>
        </Form>
    );
}