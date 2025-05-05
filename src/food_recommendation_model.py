import tensorflow as tf

@tf.keras.utils.register_keras_serializable()
class FoodRecommendationModel(tf.keras.Model):
    def __init__(self, child_input_dim, food_input_dim, **kwargs):
        super(FoodRecommendationModel, self).__init__(**kwargs)

        self.child_encoder = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(child_input_dim,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(16, activation='linear')
        ])

        self.food_encoder = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(food_input_dim,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(16, activation='linear')
        ])

        self.child_input_dim = child_input_dim
        self.food_input_dim = food_input_dim

    def call(self, inputs):
        child_input, food_input = inputs
        child_embedding = self.child_encoder(child_input)
        food_embedding = self.food_encoder(food_input)
        child_norm = tf.norm(child_embedding, axis=1, keepdims=True)
        food_norm = tf.norm(food_embedding, axis=1, keepdims=True)
        similarity = tf.matmul(child_embedding, food_embedding, transpose_b=True) / (child_norm * tf.transpose(food_norm))
        return similarity

    def get_config(self):
        config = super(FoodRecommendationModel, self).get_config()
        config.update({
            'child_input_dim': self.child_input_dim,
            'food_input_dim': self.food_input_dim,
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)