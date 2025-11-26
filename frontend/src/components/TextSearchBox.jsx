import { Button, Form, Input } from 'antd';

const onFinishFailed = errorInfo => {
    console.log('Failed:', errorInfo);
};

export const TextSearchBox = (props) => {
    const handleSubmit = ({ Prompt }) => props.onSubmit(Prompt);

    return (
        <Form
            layout="vertical"
            style={{
                maxWidth: 600,
                width: '100%',
                textAlign: 'center',
            }}
            initialValues={{ remember: true }}
            onFinish={handleSubmit}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
        >
            <Form.Item
                label="Pesquise seu imóvel ideal"
                name="Prompt"
                style={{ width: '100%' }}
                rules={[{ required: true, message: 'Por favor, digite algo!' }]}
            >
                <Input />
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Pesquisar
                </Button>
            </Form.Item>
        </Form>

    );
}