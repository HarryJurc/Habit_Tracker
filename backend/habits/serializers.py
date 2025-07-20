from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    linked_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        execution_time = data.get("execution_time")
        if execution_time and execution_time > 120:
            raise serializers.ValidationError("Время выполнения не может превышать 120 секунд.")

        periodicity = data.get("periodicity")
        if periodicity and not (1 <= periodicity <= 7):
            raise serializers.ValidationError("Периодичность — от 1 до 7 дней.")

        is_pleasant = data.get("is_pleasant", False)
        reward = data.get("reward")
        linked_habit = data.get("linked_habit")

        if is_pleasant:
            if reward or linked_habit:
                raise serializers.ValidationError("Приятная привычка не может иметь награду или связанную привычку.")
        else:
            if reward and linked_habit:
                raise serializers.ValidationError("Можно указать либо награду, либо связанную привычку, но не оба.")
            if linked_habit and not linked_habit.is_pleasant:
                raise serializers.ValidationError("Связанная привычка должна быть приятной.")

        return data
