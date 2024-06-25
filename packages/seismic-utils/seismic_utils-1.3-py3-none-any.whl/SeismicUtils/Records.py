"""
地震动记录类，采用GroundMotion包选波得到的实例属于该类，与生存的pickle波库配套使用
"""
from typing import Literal
from PIL import Image
from pathlib import Path
import dill as pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from SeismicUtils import calculus


class Records:
    def __init__(self, name: str=None):
        self.name: str = name  # 小波库名
        self.N_gm: int = 0  # 地震动数量
        self.info: pd.DataFrame = None  # 地震动信息
        self.unscaled_data: list[np.ndarray] = []  # 未缩放时程序列
        self.unscaled_spec: list[np.ndarray] = []  # 未缩放反应谱数据
        self.SF: list[float] = []  # 缩放系数
        self.dt: list[float] = []  # 步长
        self.type_: list[Literal['A', 'V', 'D']] = []  # 数据类型(加速度, 速度, 位移)
        self.selecting_text: str = None
        self.target_spec: np.ndarray = None  # 目标谱(2列, 周期&加速度谱值)
        self.individual_spec: np.ndarray = None  # 各条波反应谱(1+N列, 周期&多列加速度谱值)
        self.mean_spec: np.ndarray = None  # 平均谱(2列, 周期&平均加速度谱值)
        self.img: Image = None  # 反应谱对比图

    def _add_record(self,
            unscaled_data: np.ndarray,
            unscaled_spec: np.ndarray,
            SF: float,
            dt: float,
            type_: Literal['A', 'V', 'D']):
        """记录一条地震动

        Args:
            unscaled_data (np.ndarray): 无缩放的时程序列
            unscaled_spec (np.ndarray): 无缩放的反应谱
            SF (float): 缩放系数
            dt (float): 步长
            type_ (Literal['A', 'V', 'D']): 数据类型(加速度, 速度, 位移)
        """
        self.N_gm += 1
        self.unscaled_data.append(unscaled_data)
        self.unscaled_spec.append(unscaled_spec)
        self.SF.append(SF)
        self.dt.append(dt)
        self.type_.append(type_)

    def _to_pkl(self, file_name: str, folder: Path | str):
        """导出实例到pkl文件

        Args:
            file_name (str): 文件名(不带后缀)
            folder (Path | str): 文件夹路径
        """
        print(f'正在写入pickle文件...\r', end='')
        folder = Path(folder)
        if not folder.exists():
            raise FileExistsError(f'{str(folder.absolute())}不存在！')
        with open(folder / f'{file_name}.pkl', 'wb') as f:
            pickle.dump(self, f)
            # pickle.dump(Records, f)
        print(f'已导出pickle文件            ')

    def plot_spectra(self):
        """绘制反应谱曲线
        """
        T = self.individual_spec[:, 0]
        label = 'Individual'
        for col in range(1, self.individual_spec.shape[1]):
            Sa = self.individual_spec[:, col]
            plt.plot(T, Sa, color='#A6A6A6', label=label)
            if label:
                label = None
        plt.plot(self.target_spec[:, 0], self.target_spec[:, 1], label='Target', color='black', lw=3)
        plt.plot(self.mean_spec[:, 0], self.mean_spec[:, 1], color='red', label='Mean', lw=3)
        plt.xlim(min(self.target_spec[:, 0]), max(self.target_spec[:, 0]))
        plt.title('Selected records')
        plt.xlabel('T [s]')
        plt.ylabel('Sa [g]')
        plt.legend()
        plt.show()

    def get_unscaled_records(self) -> zip:
        """导出未缩放的时程

        Returns:
            zip[tuple[np.ndarray, float]]: 时程序列，步长

        Examples:
            >>> for data, dt in get_unscaled_records():
                    print(data.shape, dt)
        """
        return zip(self.unscaled_data, self.dt)

    def get_scaled_records(self) -> zip:
        """导出缩放后的时程

        Returns:
            zip[tuple[np.ndarray, float]]: 时程序列，步长

        Examples:
            >>> for data, dt in get_scaled_records():
                    print(data.shape, dt)
        """
        scaled_data = []
        for i, sf in enumerate(self.SF):
            scaled_data.append(self.unscaled_data[i] * sf)
        return zip(scaled_data, self.dt)
        
    def get_normalised_records(self) -> zip:
        """导出归一化的时程

        Returns:
            zip[tuple[np.ndarray, float]]: 时程序列，步长

        Examples:
            >>> for data, dt in get_normalised_records():
                    print(data.shape, dt)
        """
        normalised_data = []
        for i in range(self.N_gm):
            normalised_data.append(self._normalisation(self.unscaled_data[i]))
        return zip(normalised_data, self.dt)

    @staticmethod
    def _normalisation(data: np.ndarray):
        return data / np.max(np.abs(data))
    
    def show_info(self):
        """展示地震动信息"""
        print(f'Number of ground motions: {self.N_gm}\n')
        print(self.info)

    def get_record_name(self) -> list[str]:
        """获取地震动名称

        Returns:
            list[str]: 地震动名称
        """
        return self.info['earthquake_name'].to_list()